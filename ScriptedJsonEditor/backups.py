""" Back up old files to temp directory"""

from datetime import datetime
from os import rename, path, makedirs
from tempfile import gettempdir

# pylint: disable=too-few-public-methods
class Backups(object):
  """ Back up old files to temp directory"""
  def __init__(self):
    self.tempdir = path.join(gettempdir(), 'ScriptedJsonEditor')
    makedirs(self.tempdir, exist_ok=True)

  def backup_file(self, filename):
    """ Back up 'filename' to <temp dir>'filename'.YYYYMMDD-HHMMSS """
    _timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    _filename = '.'.join([path.basename(filename), _timestamp])
    _backup = path.join(self.tempdir, _filename)
    if not path.exists(_backup):
      # more than one back up file created in the same second
      # don't bother, keep the older one
      rename(filename, _backup)
    return _backup
