from command_line import CommandLine
import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(
    0, os.path.abspath(
        os.path.dirname(
            os.path.dirname(
                os.path.realpath(__file__)))))


class Test_test_command_line(unittest.TestCase):
    # Mock the print call in CommandLine()
    @patch('command_line.print', create=True)
    # Note added , print_ to mock print()
    def test_command_line_no_jobs_file_specified(self, print_):
        sys.argv = ['ScriptedJsonEditor']
        with patch('builtins.input', return_value=''):
            self.CLo = CommandLine()
        jobsFile = self.CLo.get_jobs_file()
        assert jobsFile is None, jobsFile

    '''
    No job file in command line now calls the GUI
    @patch('command_line.print', create=True)                   # Mock the print call in CommandLine()
    def test_command_line_jobs_file_entered(self, print_):      # Note added , print_ to mock print()
        """ Test console entry of the job file name """
        sys.argv = ['ScriptedJsonEditor']
        with patch('builtins.input', return_value='JsonEditorJobs.json'):
          self.CLo = CommandLine()
        jobsFile = self.CLo.get_jobs_file()
        assert jobsFile == 'JsonEditorJobs.json', jobsFile
    '''

    def test_command_line(self):
        sys.argv = ['ScriptedJsonEditor', 'JsonEditorJobs.json']
        self.CLo = CommandLine()
        jobsFile = self.CLo.get_jobs_file()
        assert jobsFile == 'JsonEditorJobs.json', jobsFile


if __name__ == '__main__':

    unittest.main()
