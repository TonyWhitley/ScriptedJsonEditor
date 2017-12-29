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
  def read(self, filepath):
    """ Read the JSON file """
    try:
      with open(filepath) as f_p:
        try:
          self.json_dict = json.load(f_p)
          self.filepath = filepath
          return self.json_dict
        except ValueError:
          print('JSON content error in "%s"' % filepath)
    except IOError:
      print('Failed to open JSON file "%s"' % filepath)

  def write(self, filepath):
    """ Write the JSON file, maintaining the rFactor 2 JSON "style" """
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

    with open(filepath, 'w') as f_p:
      f_p.write('\n'.join(_whitespace_removed))

  def edit(self, main_key, sub_key, new_value):
    """ Change the value of 'main_key''sub_key' in the JSON file to 'new_value' """
    if '#' in sub_key:
      pass # it's a "comment main_key"
    else:
      try:
        self.json_dict[main_key][sub_key] = new_value
      except KeyError:
        print('No such sub key "%s":"%s"' % (main_key, sub_key))

  def get_jobs(self):
    """
    Get the list of jobs in this JSON dict
    """
    jobs = [self.json_dict[key] for key in self.json_dict if 'job' in key.lower()]
    return jobs

  def run_jobs(self, jobs):
    """
    Execute the list of jobs in this JSON dict
    """
    for job in jobs:
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



if __name__ == '__main__':
  # Read command line
  # Execute
  pass
