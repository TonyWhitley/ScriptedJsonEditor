""" Parse the command line """
import sys

class CommandLine(object):
  """description of class"""
  def __init__(self):
    if len(sys.argv) > 1:
      self.jobs_file = sys.argv[1]
    else:
      print('%s <jobs file name>' % sys.argv[0])

  def get_args(self):
    """ get the command line args """
    return self.jobs_file

  # pylint: disable=no-self-use
  def get_options(self):
    """ when there are some """
    return None
