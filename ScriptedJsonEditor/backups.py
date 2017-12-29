""" Back up old files to temp directory"""

from datetime import datetime
from os import rename, path
from tempfile import gettempdir

# pylint: disable=too-few-public-methods
class Backups(object):
  """ Back up old files to temp directory"""
  def __init__(self):
    self.tempdir = gettempdir()
  def backup_file(self, filename):
    """ Back up 'filename' to <temp dir>'filename'.YYYYMMDD-HHMMSS """
    _timestamp = datetime.now().strftime('%Y%M%d-%H%M%S')
    _filename = '.'.join([path.basename(filename), _timestamp])
    _backup = path.join(self.tempdir, _filename)
    rename(filename, _backup)
    return _backup
