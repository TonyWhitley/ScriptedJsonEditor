""" Parse the command line """
import sys

jobsJSONhelpStr = r"""
{"job1":
  {
  "JSONfileToBeEdited": "c:\\Program Files (x86)\\Steam\\steamapps\\common\\rFactor 2\\UserData\\player\\player.json",
  "skip keys with # in them": true,
  "# keys with # in them are used as comments, don't change the values": 0,
  "rFactor escape slash": true,
  "# rFactor 2 escapes /. Also remove space after the :": 0,

  "edits": {
    "Graphic Options":{
        "Allow Letterboxing":false,
        "Allow Letterboxing#":"whether we allow letterboxing (during replays, for example)",
        "Automap":3,
        "Automap#":"0=off 1=race-only 2=non-race-only 3=all sessions"
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
        """%s <jobs file name> 
        
        Jobs file is a JSON file specifying the JSON file to be edited 
        and the edits to be performed. Example contents:

        %s
        """ % (sys.argv[0], jobsJSONhelpStr))

  def get_jobs_file(self):
    """ get the jobs file from the command line """
    return self.jobs_file

  # pylint: disable=no-self-use
  def get_options(self):
    """ when there are some """
    return None
