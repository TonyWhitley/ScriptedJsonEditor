import os
import sys
import unittest

import ScriptedJsonEditor
import backups

PLAYER_JSON = r'c:\Program Files (x86)\Steam\steamapps\common\rFactor 2\UserData\player\Player.JSON'
CONTROLLER_JSON = r'c:\Program Files (x86)\Steam\steamapps\common\rFactor 2\UserData\player\Controller.JSON'

EDITS_EXAMPLE = [
  # General graphics
  ("Graphic Options", "Track Detail", 1),  # "0=Low 1=Medium 2=High 3=Full"
  ("Graphic Options", "Player Detail", 1),
  ("Graphic Options", "Opponent Detail", 1),
  ("Graphic Options", "Texture Detail", 1),
  ("Graphic Options", "Texture Filter", 4),  # "0, bilinear, 1, trilinear, 2,
                                             # X2 AF, 3, X4 AF, 4, X8 AF, 5, X16 AF"
  ]

class Test_test_whole_program(unittest.TestCase):
  def test_using_test_dict(self):
    if os.path.exists(PLAYER_JSON):
      _JSNO_O = ScriptedJsonEditor.JsonFile()
      P_JSON = _JSNO_O.read(PLAYER_JSON)
      ##################################
      # change values as required
      ##################################
      for key, item, newValue in EDITS_EXAMPLE:
        _JSNO_O.edit(key, item, newValue)

      _PLAYER_JSON = PLAYER_JSON + '.edited'
      _JSNO_O.write(_PLAYER_JSON)
      assert os.path.exists(_PLAYER_JSON), _PLAYER_JSON

  def test_whole_example_job(self):
    sys.argv = ['ScriptedJsonEditor', 'jobs\\VR_G25.json']
    try:
      _backupO = backups.Backups()
      _backupFilename = _backupO.backup_file(PLAYER_JSON, _keep_the_original=True)
      _backupFilename = _backupO.backup_file(CONTROLLER_JSON, _keep_the_original=True)
      
      _exit_code = ScriptedJsonEditor.main()

      # check the changes were made
      _JSNO_O = ScriptedJsonEditor.JsonRfactorFile()
      _player = _JSNO_O.read(PLAYER_JSON)
      #assert _player["Graphic Options"]["Allow Letterboxing"] == False, _player["Graphic Options"]["Allow Letterboxing"]
      #assert _player["Graphic Options"]["Automap"] == 3, _player["Graphic Options"]["Automap"]

    finally:
      # restore the original player.JSON
      _backupO.restore_last_backup(PLAYER_JSON)
      _backupO.restore_last_backup(CONTROLLER_JSON)

    assert _exit_code == 0

  
if __name__ == '__main__':
    unittest.main()
