""" Parse the command line """
import argparse
import json
import os
import sys

configFile = 'ScriptedJsonEditorCfg.json' # file in same directory as exe

JOBS_FILE_HELP_STR = r"""
{
  "<PLAYER.JSON>": "c:\\Program Files (x86)\\Steam\\steamapps\\common\\rFactor 2\\UserData\\Player\\player.JSON",
  "jobs file format": 6,
  "job definition files": [
    "job_definitions\\demo_jobs.json"
  ],
  "jobs": [
    {
      "demo_jobs": [
        "Letterboxing off",
        "Map 2"
      ]
    }
  ]
}
"""

JOB_DEFINITIONS_FILE_HELP_STR = r"""
{
  "#Tooltip: Demo_jobs - job definitions file for ScriptedJsonEditor": 0,
  "# V1.0.0": 0,
  "# Note: any key with a # is a comment": 0,
  "job definitions": {
    "Letterboxing off": {
      "JSONfileToBeEdited": "<PLAYER.JSON>",
      "edits": {
      "Graphic Options":{
          "Allow Letterboxing":false,
          "Allow Letterboxing#":"whether we allow letterboxing (during replays, for example)"
        }
      }
    },
    "Map 2": {
      "JSONfileToBeEdited": "<PLAYER.JSON>",
      "edits": {
      "Graphic Options":{
          "Automap":2,
          "Automap#":"0=off 1=race-only 2=non-race-only 3=all sessions"
        }
      }
    }
  }
}
"""

class CommandLine(object):
  """description of class"""
  def __init__(self, versionStr=''):
    self.jobs_file = None
    self.player = 'player'
    self.rF2root = '%ProgramFiles(x86)%/Steam/steamapps/common/rFactor 2'
    try:
      self.parser = argparse.ArgumentParser(prog = versionStr,
                                            description = 'JSON file editor')
      self.parser.add_argument('filename',  
                                nargs='?', # optional
                                help =            """
%s <jobs file name>

<jobs file name> is a JSON file specifying the JSON file to be edited
and the edits to be performed. This you edit to your requirements.
Example contents:

%s

That makes use of the one of the "Jobs definition files" demo_jobs.json
that handles the details of the edits.  These files are shared (though you
are of course free to edit them).
Example contents of that are:
%s
        """ % (sys.argv[0], JOBS_FILE_HELP_STR, JOB_DEFINITIONS_FILE_HELP_STR))
      # Args with values
      self.parser.add_argument('-p', '--player', 
                               help = 'Optional: player ID (default "player")')
      
      self.args = self.parser.parse_args()
    except:
      print('\nCommand line parsing failed.')
      sys.exit(99)

    if os.path.isfile(configFile):
      with open(configFile) as fp:
        try:
          _str = fp.read()  # read separately so it can be mocked.
          _json_dict = json.loads(_str)
          self.player = _json_dict['player']
          self.rF2root = _json_dict['rF2root']
          pass
        except:
          print(sys.exc_info()[0])
          pass


    if self.args.player:
      self.player = self.args.player
    if self.args.filename:
      if self.args.filename[-5:].lower() == '.json':
        self.jobs_file = self.args.filename
      else:
        self.jobs_file = input('Enter jobs file name (just Enter to quit): ')
    else:
      self.jobs_file = None  # Run the GUI

    

  def get_jobs_file(self):
    """ get the jobs file from the command line """
    return self.jobs_file

  def get_playerID(self):
    """ get the player ID from the default/config file/command line """
    return self.player

  def get_rF2root(self):
    """ get the rF2root from the default/config file """
    return os.path.normpath(os.path.expandvars(self.rF2root))

  # pylint: disable=no-self-use
  def get_options(self):
    """ when there are some """
    return None
