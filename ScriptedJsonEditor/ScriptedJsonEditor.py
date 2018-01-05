# pylint: disable=invalid-name
# Warning		Module name "ScriptedJsonEditor" doesn't conform to snake_case naming style

"""
 Scripted JSON editor to make changes for example to rFactor 2 player.json
 1) Read the file
 2) edit("Graphic Options", "Track Detail", 1)
    Repeat as necessary
 3) Write the file
"""

import json
import sys

from backups import Backups
from command_line import CommandLine

BUILD_REVISION = 30 # The git commit count

# User-defined exceptions
class EmptyJsonError(Exception):
  """ The JSON string (usually loaded from a .JSON file) is empty """
  pass

class JsonContentError(Exception):
  """ The JSON string (usually loaded from a .JSON file) is invalid in some way """
  pass


class JsonFile():
  """
  Read, write and edit a JSON file.
  """
  def __init__(self):
    self.json_dict = None
    self.filepath = None
    self.config = {
      "skip keys with # in them": True
    }

  def read(self, filepath):
    """ Read the JSON file """
    try:
      with open(filepath) as f_p:
        try:
          self.json_dict = json.load(f_p)
          self.filepath = filepath
          return self.json_dict
        except ValueError as err:
          print('JSON content error in "%s"' % filepath)
          print(err)
    except IOError:
      print('Failed to open JSON file "%s"' % filepath)
    raise JsonContentError

  def write(self, _filepath=None):
    """ Write the JSON file
    _filepath is for unit testing
    """
    _json_txt = json.dumps(self.json_dict, indent=2)
    self._write_json_text(_json_txt, _filepath)

  def _write_json_text(self, json_txt, filepath=None):
    if filepath is None:
      filepath = self.filepath
    with open(filepath, 'w') as f_p:
      try:
        f_p.write(json_txt)
      except IOError:
        print('Failed to write JSON file "%s"' % filepath)
        # ToDo: restore back up?

  def edit(self, main_key, sub_key, new_value):
    """
    Change the value of 'main_key''sub_key' in the JSON file to 'new_value'
    May raise KeyError, ValueError or EmptyJsonError
    """
    if self.json_dict is None:
      print('Empty JSON file "%s"' % self.filepath)
      raise EmptyJsonError

    if '#' in sub_key and self.config["skip keys with # in them"]:
      pass # it's a "comment main_key"
    else:
      # check that key exists, otherwise it's a typo in the job
      if main_key in self.json_dict:
        if sub_key in self.json_dict[main_key]:
          try:
            self.json_dict[main_key][sub_key] = new_value
          except ValueError:
            try:
              print('Invalid value "%s" in "%s":"%s"' % (new_value, main_key, sub_key))
            except ValueError:
              print('Invalid number %d in "%s":"%s"' % (new_value, main_key, sub_key))
            raise ValueError
        else:
          print('No existing sub key "%s" in main key "%s"' % (sub_key, main_key))
          raise KeyError
      else:
        print('No existing main key "%s":"%s"' % (main_key, sub_key))
        raise KeyError

  def _load(self, json_str):
    """ For unit tests - load the JSON dict with values to be edited """
    try:
      self.json_dict = json.loads(json_str)
      self.filepath = 'from string'
      return self.json_dict
    except ValueError:
      print('JSON string content error in _load()')
      raise ValueError

  def _get_value(self, main_key, sub_key):
    """ For unit tests - get value of dict key """
     # pylint: disable=no-else-return
    if main_key in self.json_dict:
      if sub_key in self.json_dict[main_key]:
        return self.json_dict[main_key][sub_key]
      else:
        print('Sub key "%s" not in main key "%s"' % (sub_key, main_key))
        return None
    else:
      print('Main key "%s" not in JSON dict' % main_key)
      return None

class JsonJobsFile(JsonFile):
  """
  Get a list of keys whose name contains "job" and use those to
  edit the file.
  """
  def __init__(self):
    # default to rfactor 2 player.json filepath and formatting:
    super().__init__()
    self.config = \
      {"JSONfileToBeEdited":
       r"c:\Program Files (x86)\Steam\steamapps\common\rFactor 2\UserData\player\player.json",
       "skip keys with # in them": True,
       "rFactor escape slash": True
      }

  def read(self, filepath):
    self.json_dict = super().read(filepath)
    if self.json_dict:
      for key in ["JSONfileToBeEdited",
                  "skip keys with # in them",
                  "rFactor escape slash"]:
        if key in self.json_dict:
          self.config[key] = self.json_dict[key]
    return self.json_dict

  def get_jobs(self):
    """
    Get the list of jobs in this JSON dict
    """
    _result = []
    for _job in self.json_dict["jobs"]:
      _result.append(self.json_dict[_job])
    return _result

class JsonRfactorFile(JsonFile):
  """
  Use rfactor 2 player.json formatting:
  """
  def write(self, _filepath=None):
    """ Write the JSON file, maintaining the rFactor 2 JSON "style"
    _filepath is for unit testing
    """
    _json_txt = json.dumps(self.json_dict, indent=2).splitlines()
    # json.dumps() puts a space after the :  rF2 doesn't
    # So strip it out to make it easier to compare before and after
    _whitespace_removed = []
    for _line in _json_txt:
      _line = _line.replace(': ', ':', 1)

      # For some reason rF2 escapes / in values
      _colon = _line.find(':')
      if _colon:
        _line = _line[:_colon] + _line[_colon:].replace('/', r'\/')
      _whitespace_removed.append(_line)
    _json_txt = '\n'.join(_whitespace_removed)

    super()._write_json_text(_json_txt, _filepath)

class Job():
  """ Run a job """
  def __init__(self, job):
    self.job = job
    if 'rFactor escape slash' in job and job['rFactor escape slash']:
      self.json_o = JsonRfactorFile()
    else:
      self.json_o = JsonFile()

  def read_json_file_to_be_edited(self):
    """
    Read the file specified by the job file key 'JSONfileToBeEdited'
    May raise JsonContentError
    """
    self.json_o.read(self.job["JSONfileToBeEdited"])

  def _load(self, json_str):
    """ For unit tests - load the JSON dict with values to be edited """
    # pylint: disable=protected-access
    return self.json_o._load(json_str)

  def _get_value(self, main_key, sub_key):
    # pylint: disable=protected-access
    return self.json_o._get_value(main_key, sub_key)

  def run_edits(self):
    """
    Execute the job's edits on current file
    May raise KeyError or ValueError
    """
    for main_key in self.job["edits"]:
      for _item in self.job["edits"][main_key]:
        self.json_o.edit(main_key, _item, self.job["edits"][main_key][_item])

  def backup_file(self):
    """ Move file to datestamped file in temp folder """
    _backupO = Backups()
    _backupFilename = _backupO.backup_file(self.job["JSONfileToBeEdited"])
    return 'Original file %s backed up to %s' % (self.job["JSONfileToBeEdited"], _backupFilename)

  def write(self):
    """ Write the edited file """
    self.json_o.write()

def main():
  """ Main """
  _clo = CommandLine()
  jobsFile = _clo.get_jobs_file()
  if jobsFile is None:
    # No jobs file in command line
    return 1

  _JSNO_O = JsonJobsFile()
  try:
    _jobs = _JSNO_O.read(jobsFile)
  except JsonContentError:
    return 99

  if _jobs is None:
    print('No jobs in"%s"' % jobsFile)
    return 99

  # Execute
  # For each job in jobsFile
  for job in _jobs["jobs"]:
    _j = Job(_jobs[job])
    #   read the file to be edited
    try:
      _j.read_json_file_to_be_edited()
      #   do the edits
      try:
        _j.run_edits()
      except KeyError:
        break # failed, try the next job
      except ValueError:
        break # failed, try the next job
      except EmptyJsonError:
        break # failed, try the next job
      #   if successful:
      #     backup 'filepath'
      #     save new contents to 'filepath
      print(_j.backup_file())
      _j.write()
    except JsonContentError:
      print('Job %s failed opening "%s"' % (job, _jobs[job]['JSONfileToBeEdited']))
      return 99
  return 0

if __name__ == '__main__':
  print('Scripted JSON Editor V0.3.%d\n' % BUILD_REVISION)
  _result = main()
  sys.exit(_result)
