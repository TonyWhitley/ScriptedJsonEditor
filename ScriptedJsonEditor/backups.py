""" Back up old files to temp directory"""

from datetime import datetime
from os import rename, path, makedirs, remove
from shutil import copyfile
from tempfile import gettempdir

# pylint: disable=too-few-public-methods
class Backups(object):
  """ Back up old files to temp directory"""
  def __init__(self):
    self.tempdir = path.join(gettempdir(), 'ScriptedJsonEditor')
    makedirs(self.tempdir, exist_ok=True)
    self.backup = {}

  def backup_file(self, filename, _keep_the_original=False):
    """
    Back up 'filename' to <temp dir>'filename'.YYYYMMDD-HHMMSS
    _keep_the_original is for unit testing
    """
    _timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    _filename = '.'.join([path.basename(filename), _timestamp])
    self.backup[filename] = path.join(self.tempdir, _filename)
    if not path.exists(self.backup[filename]):
      # more than one back up file created in the same second
      # don't bother, keep the older one
      if not _keep_the_original:
        rename(filename, self.backup[filename])
      else:
        copyfile(filename, self.backup[filename])
    return self.backup[filename]

  def restore_last_backup(self, filename):
    """ restore the last back up of 'filename' """
    if filename in self.backup:
      if path.exists(filename):
        remove(filename)
      rename(self.backup[filename], filename)
      del self.backup[filename]
    else:
      raise FileNotFoundError
