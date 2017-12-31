import os
import unittest

import ScriptedJsonEditor

FILEPATH = r'c:\Program Files (x86)\Steam\steamapps\common\rFactor 2\UserData\player\player.json'

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
    if os.path.exists(FILEPATH):
      _JSNO_O = ScriptedJsonEditor.JsonFile()
      P_JSON = _JSNO_O.read(FILEPATH)
      ##################################
      # change values as required
      ##################################
      for key, item, newValue in EDITS_EXAMPLE:
        _JSNO_O.edit(key, item, newValue)

      _FILEPATH = FILEPATH + '.edited'
      _JSNO_O.write(_FILEPATH)
      assert os.path.exists(_FILEPATH), _FILEPATH

  
if __name__ == '__main__':
    unittest.main()
