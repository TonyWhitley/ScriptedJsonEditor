""" Test the main program """
import sys
import unittest
from unittest.mock import patch

from command_line import CommandLine
import ScriptedJsonEditor
import test_test_strings


class Test_test_main(unittest.TestCase):
  @patch('ScriptedJsonEditor.print', create=True)     # Mock the print call in main()
  def test_main_non_existent_jobs_file(self, print_): # Note added , print_ to mock print()
    sys.argv = ['ScriptedJsonEditor', 'JsonEditorJobs.json']
    assert ScriptedJsonEditor.main() != 0

  @patch('ScriptedJsonEditor.print', create=True)     # Mock the print call in main()
  @patch('command_line.print', create=True)           # Mock the print call in command_line()
  def test_main_no_jobs_file_specified(self, print_, print__): # Note added , print_ to mock print()
    sys.argv = ['ScriptedJsonEditor']
    assert ScriptedJsonEditor.main() != 0

  @patch('ScriptedJsonEditor.print', create=True)     # Mock the print call in main()
  def test_main(self, print_):                        # Note added , print_ to mock print()
    sys.argv = ['ScriptedJsonEditor', r'Tests\jobs_test1.json']
    assert ScriptedJsonEditor.main() == 0

  @patch('ScriptedJsonEditor.print', create=True)     # Mock the print call in main()
  def test_main_bad_jobs_file(self, print_):          # Note added , print_ to mock print()
    _JSNO_O = ScriptedJsonEditor.JsonFile()
    try:
      _jobs = _JSNO_O._load(test_test_strings.jobsBadJSONstr)
    except ValueError:
      return
    assert False, 'Expected job load to fail'

  @patch('ScriptedJsonEditor.print', create=True)     # Mock the print call in main()
  def test_main_key_error_in_jobs_file(self, print_): # Note added , print_ to mock print()
    _JSNO_O = ScriptedJsonEditor.JsonFile()
    try:
      _jobs = _JSNO_O._load(test_test_strings.jobsJSONstrBadKey)
    except ValueError:
      assert False, 'Expected job load to succeed'
    assert _jobs
    # Execute
    # For each job in jobsFile
    for job in _jobs["jobs"]:
      _j = ScriptedJsonEditor.Job(_jobs["jobs library"][job])
      #   read the file to be edited
      _j._load(test_test_strings.playerJSONstr)
      #   do the edits
      #   if successful:
      #     backup 'filepath'
      #     save new contents to 'filepath
      try:
        _j.run_edits()
      except KeyError:
        return # failed as expected, try the next job
      except ValueError:
        assert False, 'Didn\'t expect ValueError'
      except:
        assert False, 'Didn\'t expect other error'
    assert False, 'Expected job to fail'


  def test_main_JSONfileToBeEdited(self):
    sys.argv = ['ScriptedJsonEditor', 'jobs\\rF2VR.json']
    _clo = CommandLine()
    jobsFile = _clo.get_jobs_file()
    if jobsFile:

      _JSNO_O = ScriptedJsonEditor.JsonJobsFile()
      _JSNO_O.read(jobsFile)
      _jobs = _JSNO_O.get_jobs()

      if _jobs:
        # Execute
        # For each job in jobsFile
        for job in _jobs:
          _j = ScriptedJsonEditor.Job(job)
          #   read the file to be edited
          _j._load(test_test_strings.playerJSONstr)
      else:
        assert False, 'No jobs in jobs\\rF2VR.json'
    else:
      assert False, 'No jobsfile jobs\\rF2VR.json'

if __name__ == '__main__':
    unittest.main()
