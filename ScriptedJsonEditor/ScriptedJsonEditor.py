
"""
 Scripted JSON editor to make changes for example to rFactor 2 player.json
 1) Read the file
 2) edit("Graphic Options", "Track Detail", 1)
    Repeat as necessary
 3) Write the file
"""
import json

class JsonFile():
  def read(self, filepath):
    try:
      with open(filepath) as fp:
        try:
          self.JsonDict = json.load(fp)
          self.filepath = filepath
          return self.JsonDict
        except:
          print('JSON content error in "%s"' % filepath)
    except:
      print('Failed to open JSON file "%s"' % filepath)

  def write(self, filepath):
    _json_txt = json.dumps(self.JsonDict, indent = 2).splitlines()
    # json.dumps() puts a space after the :  rF2 doesn't
    # So strip it out to make it easier to compare before and after
    _whitespaceRemoved = []
    for _line in _json_txt:
      _line = _line.replace(': ', ':', 1)

      # For some reason rF2 escapes / in values
      _colon = _line.find(':')
      if _colon:
        _line = _line[:_colon] + _line[_colon:].replace('/', r'\/')
      _whitespaceRemoved.append(_line)

    with open(filepath, 'w') as fp:
      fp.write('\n'.join(_whitespaceRemoved))
  
  def edit(self, main_key, sub_key, newValue):
    """ Change the value of 'main_key''sub_key' in the JSON file to 'newValue' """
    if '#' in sub_key:
      pass # it's a "comment main_key"
    else:
      try:
        self.JsonDict[main_key][sub_key] = newValue
      except:
        print('No such sub key "%s":"%s"' % (main_key, sub_key))
    pass

  def getJobs(self):
    """
    Get the list of jobs in this JSON dict
    """
    jobs = [self.JsonDict[key] for key in self.JsonDict if 'job' in key.lower()]
    return jobs

  def runJobs(self, jobs):
    """
    Execute the list of jobs in this JSON dict
    """
    for job in jobs:
      for main_key in job["edits"]:
        for item in job["edits"][main_key]:
          self.edit(main_key, item, job["edits"][main_key][item])

  def _load(self, JSONstr):
    """ For unit tests - load the JSON dict with values to be edited """
    try:
      self.JsonDict = json.loads(JSONstr)
      self.filepath = filepath
      return self.JsonDict
    except:
      print('JSON string content error in _load()')

  def _get_value(self, main_key, sub_key):
    """ For unit tests - get value of dict key """
    if main_key in self.JsonDict:
      if sub_key in self.JsonDict[main_key]:
        return self.JsonDict[main_key][sub_key]
      else:
        print('Sub key "%s" not in main key "%s"' % (sub_key, main_key))
        return None
    else:
      print('Main key "%s" not in JSON dict' % main_key)
      return None



filepath = r'c:\Program Files (x86)\Steam\steamapps\common\rFactor 2\UserData\player\player.json'

editsExample = [
    # General graphics
    ("Graphic Options", "Track Detail", 1),  # "0=Low 1=Medium 2=High 3=Full"
    ("Graphic Options", "Player Detail", 1),
    ("Graphic Options", "Opponent Detail", 1),
    ("Graphic Options", "Texture Detail", 1),
    ("Graphic Options", "Texture Filter", 4),  # "0, bilinear, 1, trilinear, 2, X2 AF, 3, X4 AF, 4, X8 AF, 5, X16 AF"
    ]

if __name__ == '__main__':
  _jsonO = JsonFile()
  pJson = _jsonO.read(filepath)
  ##################################
  # change values as required
  ##################################
  for key, item, newValue in editsExample:
    _jsonO.edit(key, item, newValue)
  
  _filepath = filepath + '.edited'
  _jsonO.write(_filepath)

  ########################## Now, what does rF2 think of the result?