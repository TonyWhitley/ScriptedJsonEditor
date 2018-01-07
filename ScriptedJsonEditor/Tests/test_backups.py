import os
from tempfile import NamedTemporaryFile
import unittest

import backups

class Test_test_backups(unittest.TestCase):
  def __create_temp_file(self):
    """ create a temporary file to back up """
    f_p = NamedTemporaryFile(delete = False)
    f_p.close()
    return f_p.name
  def test_backup(self):
    _name = self.__create_temp_file()
    # do it
    _backupO = backups.Backups()
    _backupFilename = _backupO.backup_file(_name)
    assert os.path.exists(_backupFilename), _backupFilename
    # Tidy up
    os.remove(_backupFilename)
        
  def test_restore(self):
    _backupO = backups.Backups()
    _name = []
    _backupFilename = []
    # create some files and back them up
    for i in range(2):
      _name.append(self.__create_temp_file())
      # do it
      _backupFilename.append(_backupO.backup_file(_name[i]))
      assert not os.path.exists(_name[i]), _name[i]
      assert os.path.exists(_backupFilename[i]), _backupFilename[i]

    for i in range(2):
      _backupO.restore_last_backup(_name[i])
      assert os.path.exists(_name[i]), _name[i]
      assert not os.path.exists(_backupFilename[i]), _backupFilename[i]

      # try to restore the same file again
      try:
        _backupO.restore_last_backup(_name[i])
        assert False, 'Restoring twice should error'
      except FileNotFoundError:
        # expected
        pass
      # Tidy up
      os.remove(_name[i])

  def test_restore_non_existent_file(self):
    # try to restore a file that hasn't been backed up
    _backupO = backups.Backups()
    try:
      _backupO.restore_last_backup('murgle.flurgle')
      assert False, 'Restoring file that has not been backed up should error'
    except FileNotFoundError:
      # expected
      pass
if __name__ == '__main__':
    unittest.main()
