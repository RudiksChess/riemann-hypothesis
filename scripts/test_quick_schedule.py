"""Scheduler inventory checks; no dispatches or network calls."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).with_name('quick-schedule.py')
spec = importlib.util.spec_from_file_location('quick_schedule', SCRIPT)
schedule = importlib.util.module_from_spec(spec)
spec.loader.exec_module(schedule)


class InventoryTests(unittest.TestCase):
    def inventory(self, handled=()):
        prs = [{'number': n, 'title': str(n), 'headRefOid': f'{n:040x}', 'changedFiles': 1,
                'additions': 1, 'deletions': 0, 'mergeable': 'MERGEABLE'}
               for n in range(251, 0, -1)]
        pages = [{'data': {'repository': {'pullRequests': {
            'nodes': prs[start:start + 25],
            'pageInfo': {'hasNextPage': start + 25 < len(prs), 'endCursor': str(start + 25)}
        }}}} for start in range(0, len(prs), 25)]

        def command(args, **kwargs):
            if args[:3] == ['gh', 'pr', 'list']:
                return json.dumps(prs[:int(args[args.index('--limit') + 1])])
            self.assertEqual(args[:3], ['gh', 'api', 'graphql'])
            self.assertIn('--paginate', args)
            self.assertIn('--slurp', args)
            self.assertTrue(any('after: $endCursor' in arg for arg in args))
            return json.dumps(pages)

        def gh(path):
            if path == 'rate_limit':
                return {'resources': {'core': {'remaining': 1000}}}
            self.assertIn('/runners?', path)
            return {'runners': []}

        with tempfile.TemporaryDirectory() as directory:
            state = Path(directory)
            for pr in prs:
                if pr['number'] in handled:
                    (state / (schedule.key(pr) + '.json')).write_text('{}')
            path_open = Path.open
            with (state / 'lock').open('w') as lock:
                def open_path(path, *args, **kwargs):
                    return lock if path == state / 'lock' else path_open(path, *args, **kwargs)

                with patch.object(Path, 'open', open_path), \
                     patch.object(schedule, 'command', side_effect=command), \
                     patch.object(schedule, 'gh', side_effect=gh), \
                     patch('sys.argv', [str(SCRIPT), '--state', directory, '--once']):
                    schedule.main()
            return json.loads((state / 'queue.json').read_text())

    def test_all_pages_reach_the_queue_with_existing_priority_policy(self):
        inventory = self.inventory()
        self.assertEqual([pr['pr'] for pr in inventory['waiting']],
                         [n for n in range(1, 252) if n not in schedule.PRIORITY])
        self.assertEqual({pr['pr'] for pr in inventory['deferred']}, schedule.PRIORITY)

    def test_older_requests_are_seen_after_the_newest_two_hundred_are_handled(self):
        inventory = self.inventory(handled=set(range(52, 252)))
        self.assertEqual([pr['pr'] for pr in inventory['waiting']], list(range(1, 52)))


if __name__ == '__main__':
    unittest.main()
