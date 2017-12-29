""" Test the main program """
import sys
import unittest

from ScriptedJsonEditor import main

class Test_test_main(unittest.TestCase):
  def test_main_none_existent_jobs_file(self):
    sys.argv = ['ScriptedJsonEditor', 'JsonEditorJobs.json']
    main()

  def test_main(self):
    sys.argv = ['ScriptedJsonEditor', r'C:\Users\tony_\source\repos\ScriptedJsonEditor\ScriptedJsonEditor\Tests\jobs_test1.json']
    main()


if __name__ == '__main__':
    unittest.main()
