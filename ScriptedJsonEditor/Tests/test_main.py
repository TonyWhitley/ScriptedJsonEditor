""" Test the main program """
import sys
import unittest

import ScriptedJsonEditor
import test_test_strings


class Test_test_main(unittest.TestCase):
  def test_main_non_existent_jobs_file(self):
    sys.argv = ['ScriptedJsonEditor', 'JsonEditorJobs.json']
    ScriptedJsonEditor.main()

  def test_main_no_jobs_file_specified(self):
    sys.argv = ['ScriptedJsonEditor']
    ScriptedJsonEditor.main()

  def test_main(self):
    sys.argv = ['ScriptedJsonEditor', r'C:\Users\tony_\source\repos\ScriptedJsonEditor\ScriptedJsonEditor\Tests\jobs_test1.json']
    ScriptedJsonEditor.main()

  def test_main_bad_jobs_file(self):
    _JSNO_O = ScriptedJsonEditor.JsonFile()
    try:
      _jobs = _JSNO_O._load(test_test_strings.jobsBadJSONstr)
    except ValueError:
      return
    assert False, 'Expected job load to fail'

  def test_main_key_error_in_jobs_file(self):
    _JSNO_O = ScriptedJsonEditor.JsonFile()
    try:
      _jobs = _JSNO_O._load(test_test_strings.jobsJSONstrBadKey)
    except ValueError:
      assert False, 'Expected job load to succeed'
    assert _jobs
    if _jobs:
      # Execute
      # For each job in jobsFile
      for job in _jobs:
        _PJSNO_O = ScriptedJsonEditor.JsonFile()
        _j = _jobs[job]
        #   read 'filepath'
        _filepath = _j["JSONfileToBeEdited"]
        _PJSNO_O._load(test_test_strings.playerJSONstr)
        #   do the edits
        #   if successful:
        #     backup 'filepath'
        #     save new contents to 'filepath
        try:
          _PJSNO_O.run_edits(_j)
        except KeyError:
          return # failed as expected, try the next job
        except ValueError:
          assert False, 'Didn\'t expect ValueError'
        except:
          assert False, 'Didn\'t expect other error'
      assert False, 'Expected job to fail'


if __name__ == '__main__':
    unittest.main()
