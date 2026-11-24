"""Profile counter collection and safe publication of host observations."""
import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import host_profile
from host_profile import publish_profile

class ProfileCounterTests(unittest.TestCase):
 def test_final_observation_contributes_without_a_periodic_sample(self):
  for initial,final,expected in [(10,99,99),(99,10,99),(None,99,99),(99,None,99),(None,None,None)]:
   with self.subTest(initial=initial,final=final):
    before={'cpu_usage_usec':100,'memory_current_bytes':initial,'memory_peak_bytes':None,
            'tasks_current':initial,'tasks_peak':None}
    after={**before,'cpu_usage_usec':200,'memory_current_bytes':final,'tasks_current':final}
    with patch.object(host_profile.rpc,'current_cgroup',return_value=Path('/fixture')),\
         patch.object(host_profile,'counters',side_effect=[before,after]),\
         patch.object(host_profile.threading,'Thread'):
     profile=host_profile.HostProfile().finish(2)
    self.assertEqual(profile['memory_observed_max_bytes'],expected)
    self.assertEqual(profile['tasks_observed_max'],expected)
    self.assertEqual(profile['cpu_seconds'],0.0001)
    self.assertIsNone(profile['memory_peak_bytes'])
    self.assertIsNone(profile['tasks_peak'])
    self.assertEqual(profile['exit_status'],2)

class ProfilePublicationTests(unittest.TestCase):
 def test_sandbox_symlinks_cannot_overwrite_host_sentinel(self):
  with tempfile.TemporaryDirectory()as directory:
   root=Path(directory);output=root/'job';returned=output/'returned';returned.mkdir(parents=True)
   sentinel=root/'host-sentinel';sentinel.write_text('preserve host bytes')
   (returned/'host-profile.json').symlink_to(sentinel)
   (returned/'host-profile.json.tmp').symlink_to(sentinel)
   profile={'cpu_seconds':1.25,'tasks_peak':None};publish_profile(output,profile)
   self.assertEqual(sentinel.read_text(),'preserve host bytes')
   self.assertFalse((returned/'host-profile.json').is_symlink())
   self.assertEqual(json.loads((returned/'host-profile.json').read_text()),profile)
   self.assertFalse(list(output.glob('.host-profile-*')))

if __name__=='__main__':unittest.main()
