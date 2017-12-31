""" Parse the command line """
import sys
from test_test_strings import jobsJSONstr

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
        """ % (sys.argv[0], jobsJSONstr))

  def get_jobs_file(self):
    """ get the jobs file from the command line """
    return self.jobs_file

  # pylint: disable=no-self-use
  def get_options(self):
    """ when there are some """
    return None
