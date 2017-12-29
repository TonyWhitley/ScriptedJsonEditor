from os import path
from tempfile import NamedTemporaryFile
import unittest

import backups

class Test_test_backups(unittest.TestCase):
  def test_backup(self):
    # create a temporary file to back up
    f_p = NamedTemporaryFile(delete = False)
    f_p.close()
    _name = f_p.name
    # do it
    _backupO = backups.Backups()
    _backupFilename = _backupO.backup_file(_name)
    assert path.exists(_backupFilename), _backupFilename
        

if __name__ == '__main__':
    unittest.main()
