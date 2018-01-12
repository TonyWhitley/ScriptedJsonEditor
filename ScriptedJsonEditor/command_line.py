""" Parse the command line """
import sys

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
  "# Demo_jobs - job definitions file for ScriptedJsonEditor": 0,
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
  def __init__(self):
    self.jobs_file = None
    if len(sys.argv) > 1:
      self.jobs_file = sys.argv[1]
    else:
      print(\
        """
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

      self.jobs_file = input('Enter jobs file name (just Enter to quit): ')

  def get_jobs_file(self):
    """ get the jobs file from the command line """
    return self.jobs_file

  # pylint: disable=no-self-use
  def get_options(self):
    """ when there are some """
    return None
