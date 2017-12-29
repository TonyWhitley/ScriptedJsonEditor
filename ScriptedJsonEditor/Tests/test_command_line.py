import sys
import unittest

from command_line import CommandLine

class Test_test_command_line(unittest.TestCase):
    def test_command_line(self):
        sys.argv = ['ScriptedJsonEditor', 'JsonEditorJobs.json']
        self.CLo = CommandLine()
        jobsFile = self.CLo.get_args()
        assert jobsFile == 'JsonEditorJobs.json', jobsFile

if __name__ == '__main__':

    unittest.main()
