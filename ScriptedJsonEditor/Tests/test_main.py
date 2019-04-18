""" Test the main program """
import os
import sys
import unittest
from unittest.mock import patch, mock_open

import command_line
import ScriptedJsonEditor
import test_test_strings
import backups

TEST_PLAYER_JSON = r'Tests\\player.JSON'

class Test_test_main(unittest.TestCase):
  @patch('ScriptedJsonEditor.print', create=True)     # Mock the print call in main()
  def test_main_non_existent_jobs_file(self, print_): # Note added , print_ to mock print()
    sys.argv = ['ScriptedJsonEditor', 'JsonEditorJobs.json']
    assert ScriptedJsonEditor.main()[0] != 0

  """ just calls GUI now
  @patch('ScriptedJsonEditor.print', create=True)     # Mock the print call in main()
  @patch('command_line.print', create=True)           # Mock the print call in command_line()
  def test_main_no_jobs_file_specified(self, print_, print__): # Note added , print_ to mock print()
    sys.argv = ['ScriptedJsonEditor']
    with patch('builtins.input', return_value=''):
      _exit_code, _status = ScriptedJsonEditor.main()
    assert _exit_code == 0
  """

  @patch('ScriptedJsonEditor.print', create=True)     # Mock the print call in main()
  def test_main(self, print_):                        # Note added , print_ to mock print()
    try:
      _backupO = backups.Backups()
      _backupFilename = _backupO.backup_file(TEST_PLAYER_JSON, _keep_the_original=True)

      # check before changes
      _JSNO_O = ScriptedJsonEditor.JsonRfactorFile()
      _player = _JSNO_O.read(TEST_PLAYER_JSON)
      assert _player["Graphic Options"]["Allow Letterboxing"] == True, _player["Graphic Options"]["Allow Letterboxing"]
      assert _player["Graphic Options"]["Automap"] == 3, _player["Graphic Options"]["Automap"]

      sys.argv = ['ScriptedJsonEditor', r'Tests\jobs_test1.json']

      _exit_code, _status = ScriptedJsonEditor.main()

      # check the changes were made
      _JSNO_O = ScriptedJsonEditor.JsonRfactorFile()
      _player = _JSNO_O.read(TEST_PLAYER_JSON)
      assert _player["Graphic Options"]["Allow Letterboxing"] == False, _player["Graphic Options"]["Allow Letterboxing"]
      assert _player["Graphic Options"]["Automap"] == 2, _player["Graphic Options"]["Automap"]

    finally:
      # restore the original player.JSON
      _backupO.restore_last_backup(TEST_PLAYER_JSON)

    assert _exit_code == 0

    @patch('ScriptedJsonEditor.print', create=True)     # Mock the print call in main()
    def test_main_configs_in_jobs_file(self, print_):   # Note added , print_ to mock print()
      try:
        _backupO = backups.Backups()
        _backupFilename = _backupO.backup_file(TEST_PLAYER_JSON, _keep_the_original=True)

        # check before changes
        _JSNO_O = ScriptedJsonEditor.JsonRfactorFile()
        _player = _JSNO_O.read(TEST_PLAYER_JSON)
        assert _player["Graphic Options"]["Track Detail"] == 0, _player["Graphic Options"]["Track Detail"]
        assert _player["Graphic Options"]["Texture Filter"] == 0, _player["Graphic Options"]["Texture Filter"]

        sys.argv = ['ScriptedJsonEditor', r'Tests\jobs_test_configs.json']

        _exit_code, _status = ScriptedJsonEditor.main()

        # check the changes were made
        _JSNO_O = ScriptedJsonEditor.JsonRfactorFile()
        _player = _JSNO_O.read(TEST_PLAYER_JSON)
        assert _player["Graphic Options"]["Track Detail"] == 1, _player["Graphic Options"]["Track Detail"]
        assert _player["Graphic Options"]["Texture Filter"] == 4, _player["Graphic Options"][""]

      finally:
        # restore the original player.JSON
        _backupO.restore_last_backup(TEST_PLAYER_JSON)

    assert _exit_code == 0

  @patch('ScriptedJsonEditor.print', create=True)     # Mock the print call in main()
  def test_main_bad_jobs_file(self, print_):          # Note added , print_ to mock print()
    _JSNO_O = ScriptedJsonEditor.JsonFile()
    try:
      _jobs = _JSNO_O._load(test_test_strings.jobsBadJSONstr, 'test_test_strings.jobsBadJSONstr')
    except ValueError:
      return
    assert False, 'Expected job load to fail'

  @patch('ScriptedJsonEditor.print', create=True)     # Mock the print call in main()
  def test_main_key_error_in_jobs_file(self, print_): # Note added , print_ to mock print()
    _JSNO_O = ScriptedJsonEditor.JsonFile()
    try:
      _jobs = _JSNO_O._load(test_test_strings.jobsJSONstrBadKey, 'test_test_strings.jobsJSONstrBadKey')
      config = {'rFactor escape slash': True}
    except ValueError:
      assert False, 'Expected job load to succeed'
    assert _jobs
    # Execute
    # For each job in jobsFile
    for job in _jobs["jobs"]:
      _j = ScriptedJsonEditor.Job(_jobs["job definitions"][job], config)
      #   read the file to be edited
      _j._load(test_test_strings.playerJSONstr, 'test_test_strings.playerJSONstr')
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
    sys.argv = ['ScriptedJsonEditor', 'jobs\\VR.json']
    _clo = command_line.CommandLine()
    jobsFile = _clo.get_jobs_file()
    if jobsFile:

      _JSNO_O = ScriptedJsonEditor.JsonJobsFile()
      __, config = _JSNO_O.read(jobsFile)
      _jobs = _JSNO_O.get_jobs()

      if _jobs:
        # Execute
        # For each job in jobsFile
        for job in _jobs:
          _j = ScriptedJsonEditor.Job(job, config)
          #   read the file to be edited
          _j._load(test_test_strings.playerJSONstr, 'test_test_strings.playerJSONstr')
      else:
        assert False, 'No jobs in jobs\\VR.json'
    else:
      assert False, 'No jobsfile jobs\VR.json'

  # PlayerID is defined at 3 levels:
  # * In the program:                 lowest, fallback
  # * In ScriptedJsonEditorCfg.json:  outranks the program constant
  # * In the command line switch:     outranks all
  #  Ditto for rF2path except it's not a command line switch

  def test_main_no_playerID(self):
    # The program's values
    sys.argv = ['ScriptedJsonEditor']
    _clo = command_line.CommandLine()
    _playerID = _clo.get_playerID()
    _rF2root = _clo.get_rF2root()
    assert _playerID == 'player', _playerID
    assert _rF2root == 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\rFactor 2', _rF2root

  @patch('ScriptedJsonEditor.os.path.isfile')
  def test_main_configFile_playerID(self, mock_os_isfile):
    # The config file's values
    rF2root = r"%ProgramFiles(x86)%\\Steam\\steamapps\\common\\rFactor 2CONFIG"
    sys.argv = ['ScriptedJsonEditor']
    file_content_mock = '{ "player": "playerCONFIG",\n' \
                        ' "rF2root": "%s" }' % rF2root
    fake_file_path = 'ScriptedJsonEditorCfg.json'
    #mock_os_is_file.return_value = True

    with patch('command_line.open', mock_open(read_data=file_content_mock), create=True) as m:
      _clo = command_line.CommandLine()
      _playerID = _clo.get_playerID()
      _rF2root = _clo.get_rF2root()
    assert _playerID == 'playerCONFIG', _playerID
    assert _rF2root == os.path.normpath(os.path.expandvars(rF2root)), _rF2root


  def test_main_playerID(self):
    # The command line switches
    sys.argv = ['ScriptedJsonEditor', '--player', 'playerTEST']
    _clo = command_line.CommandLine()
    _playerID = _clo.get_playerID()
    assert _playerID == 'playerTEST', _playerID

if __name__ == '__main__':
    unittest.main()
