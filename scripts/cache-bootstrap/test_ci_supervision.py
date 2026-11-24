"""Controller errors must not leave the owned build process running."""
import errno
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("ci_build", Path(__file__).parents[1] / "ci-build.py")
ci = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ci)


class SupervisionTests(unittest.TestCase):
    def assert_stopped_on_error(self, trigger):
        error = OSError(errno.ENOSPC, "fixture: no space left on device")
        command = [sys.executable, "-c", "import time; time.sleep(60)"]
        environment = os.environ.copy()
        processes = []
        popen = subprocess.Popen

        def spawn(*args, **kwargs):
            process = popen(*args, **kwargs)
            processes.append(process)
            if trigger == "interrupt":
                wait = process.wait
                def interrupted_once(*args, **kwargs):
                    process.wait = wait
                    raise KeyboardInterrupt
                process.wait = interrupted_once
            return process

        with tempfile.TemporaryFile() as stream:
            class FullLog:
                def fileno(self):
                    return stream.fileno()
                def write(self, data):
                    return stream.write(data)
                def flush(self):
                    raise error

            disk = [SimpleNamespace(free=2 * 1024**3), SimpleNamespace(free=0)]
            try:
                with patch.object(ci.subprocess, "Popen", side_effect=spawn), \
                     patch.object(ci.shutil, "disk_usage", side_effect=disk), \
                     patch.object(ci, "sync_visible_log", side_effect=error if trigger == "mirror" else None):
                    with self.assertRaises(OSError) as caught:
                        ci.supervised_build(command, environment, FullLog(), [Path(".")], 1,
                                            timeout_seconds=0 if trigger == "timeout" else None)
                self.assertIs(caught.exception, error)
                self.assertEqual(len(processes), 1)
                self.assertIsNotNone(processes[0].returncode, "controller did not stop and reap its build")
            finally:
                for process in processes:
                    if process.poll() is None:
                        ci.stop_build_process(process, command, environment)

    def test_failed_stop_message_still_stops_the_build(self):
        for trigger in ("disk", "timeout", "interrupt"):
            with self.subTest(trigger=trigger):
                self.assert_stopped_on_error(trigger)

    def test_failed_log_mirror_still_stops_the_build(self):
        self.assert_stopped_on_error("mirror")

    def test_completed_build_does_not_need_a_stop_signal(self):
        with tempfile.TemporaryFile() as log, patch.object(ci, "stop_build_process") as stop:
            code = ci.supervised_build([sys.executable, "-c", "pass"], os.environ.copy(), log, [], 0)
        self.assertEqual(code, 0)
        stop.assert_not_called()


if __name__ == "__main__":
    unittest.main()
