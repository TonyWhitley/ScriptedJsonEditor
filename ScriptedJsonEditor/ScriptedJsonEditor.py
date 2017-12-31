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

from backups import Backups
from command_line import CommandLine

class JsonFile():
  """
  Read, write and edit a JSON file.
  Also get a list of keys whose name contains "job" and use those to
  edit the file.
  Maintains rFactor 2 JSON "style" - e.g. escaping /
  """
  def __init__(self):
    self.json_dict = None
    self.filepath = None
    # default to rfactor 2 player.json filepath and formatting:
    self.config = \
      {"JSONfileToBeEdited":
       r"c:\Program Files (x86)\Steam\steamapps\common\rFactor 2\UserData\player\player.json",
       "skip keys with # in them": True,
       "rFactor escape slash": True
      }

  def read(self, filepath):
    """ Read the JSON file """
    try:
      with open(filepath) as f_p:
        try:
          self.json_dict = json.load(f_p)
          self.filepath = filepath
          for key in ["JSONfileToBeEdited",
                      "skip keys with # in them",
                      "rFactor escape slash"]:
            if key in self.json_dict:
              self.config[key] = self.json_dict[key]
          return self.json_dict
        except ValueError:
          print('JSON content error in "%s"' % filepath)
    except IOError:
      print('Failed to open JSON file "%s"' % filepath)

  def backup_file(self):
    """ Move file to datestamped file in temp folder """
    _backupO = Backups()
    _backupFilename = _backupO.backup_file(self.filepath)
    print('Original file %s backed up to %s' % (self.filepath, _backupFilename))

  def write(self, _filepath=None):
    """ Write the JSON file, maintaining the rFactor 2 JSON "style"
    _filepath is for unit testing
    """
    _json_txt = json.dumps(self.json_dict, indent=2).splitlines()
    if self.config["rFactor escape slash"]:
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
    #else no reformatting required

    if _filepath is None:
      _filepath = self.filepath
    with open(_filepath, 'w') as f_p:
      f_p.write(_json_txt)

  def edit(self, main_key, sub_key, new_value):
    """
    Change the value of 'main_key''sub_key' in the JSON file to 'new_value'
    May raise KeyError
    """
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
        else:
          print('No existing sub key "%s" in main key "%s"' % (sub_key, main_key))
          raise KeyError
      else:
        print('No existing main key "%s":"%s"' % (main_key, sub_key))
        raise KeyError

  def get_jobs(self):
    """
    Get the list of jobs in this JSON dict
    """
    jobs = [self.json_dict[key] for key in self.json_dict if 'job' in key.lower()]
    return jobs

  def read_json_file_to_be_edited(self):
    """ Read the file specified by the job file key 'JSONfileToBeEdited' """
    self.read(self.config["JSONfileToBeEdited"])

  def run_edits(self, job):
    """
    Execute the job's edits on current file
    May raise KeyError or ValueError
    """
    for main_key in job["edits"]:
      for _item in job["edits"][main_key]:
        self.edit(main_key, _item, job["edits"][main_key][_item])

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

def main():
  """ Main """
  print('Scripted JSON Editor V0.1.17\n')
  _clo = CommandLine()
  jobsFile = _clo.get_args()

  _JSNO_O = JsonFile()
  _jobs = _JSNO_O.read(jobsFile)

  # this needs tidying. Why does 'job' only contain the name of the job
  # and not the associated data???
  if _jobs:
    # Execute
    # For each job in jobsFile
    for job in _jobs:
      _PJSNO_O = JsonFile()
      _j = _jobs[job]
      #   read the file to be edited
      _PJSNO_O.read_json_file_to_be_edited()
      #   do the edits
      #   if successful:
      #     backup 'filepath'
      #     save new contents to 'filepath
      try:
        _PJSNO_O.run_edits(_j)
      except KeyError:
        break # failed, try the next job
      except ValueError:
        break # failed, try the next job
      _PJSNO_O.backup_file()
      _PJSNO_O.write()

if __name__ == '__main__':
  main()
