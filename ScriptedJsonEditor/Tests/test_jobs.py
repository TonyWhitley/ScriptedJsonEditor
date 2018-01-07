import os
import sys
import unittest
from unittest.mock import patch

import test_test_strings

import ScriptedJsonEditor

this_folder = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

def this_path(filename):
  return os.path.join(this_folder, filename)

class Test_test_jobs(unittest.TestCase):
    @patch('ScriptedJsonEditor.print', create=True)   # Mock the print call in ScriptedJsonEditor()
    def test_read_0(self, print_):                    # Note added , print_ to mock print()
        filepath = this_path('no_such_file.json')
        _JSNO_O = ScriptedJsonEditor.JsonJobsFile()
        try:
          P_JSON = _JSNO_O.read(filepath)
        except FileNotFoundError:
          pass
        except ScriptedJsonEditor.JsonContentError:
          pass
    def test_read_file(self):
        filepath = this_path('jobs_test1.json')
        _JSNO_O = ScriptedJsonEditor.JsonJobsFile()
        P_JSON, config = _JSNO_O.read(filepath)
        assert P_JSON["jobs library"]["job1"] != None
        assert P_JSON["jobs library"]["job1"]["JSONfileToBeEdited"] != None
        assert len(P_JSON["jobs library"]["job1"]["edits"]) > 0, P_JSON["jobs library"]["job1"]["edits"]
    def test_load_JSON_str(self):
        _JSNO_O = ScriptedJsonEditor.JsonJobsFile()
        _JSNO_O._load(test_test_strings.jobsJSONstr1)
        P_JSON, config = _JSNO_O._read()
        assert P_JSON["jobs library"]["job1"] != None
        assert P_JSON["jobs library"]["job1"]["JSONfileToBeEdited"] != None
        assert len(P_JSON["jobs library"]["job1"]["edits"]) > 0, P_JSON["jobs library"]["job1"]["edits"]
    def test_get_jobs(self):
        _JSNO_O = ScriptedJsonEditor.JsonJobsFile()
        _JSNO_O._load(test_test_strings.jobsJSONstr1)
        P_JSON, config = _JSNO_O._read()
        assert P_JSON["jobs library"]["job1"] != None
        assert P_JSON["jobs library"]["job1"]["JSONfileToBeEdited"] != None
        assert len(P_JSON["jobs library"]["job1"]["edits"]) > 0, P_JSON["jobs library"]["job1"]["edits"]
        jobs = _JSNO_O.get_jobs()
        assert len(jobs) > 0
        assert jobs[0]["JSONfileToBeEdited"] != None
        assert len(jobs[0]["edits"]) > 0, jobs[0]["edits"]

    def test_load_JSON_str_2jobs(self):
        _JSNO_O = ScriptedJsonEditor.JsonJobsFile()
        _JSNO_O._load(test_test_strings.jobsJSONstrBadKey2)
        P_JSON, config = _JSNO_O._read()
        assert P_JSON["jobs library"]["job1"] != None
        assert P_JSON["jobs library"]["job1"]["JSONfileToBeEdited"] != None
        assert len(P_JSON["jobs library"]["job1"]["edits"]) > 0, P_JSON["jobs library"]["job1"]["edits"]
        assert P_JSON["jobs library"]["job2"] != None
        assert P_JSON["jobs library"]["job2"]["JSONfileToBeEdited"] != None
        assert len(P_JSON["jobs library"]["job2"]["edits"]) > 0, P_JSON["jobs library"]["job2"]["edits"]
    def test_get_2jobs(self):
        _JSNO_O = ScriptedJsonEditor.JsonJobsFile()
        _JSNO_O._load(test_test_strings.jobsJSONstrBadKey2)
        P_JSON, config = _JSNO_O._read()
        assert P_JSON["jobs library"]["job1"] != None
        assert P_JSON["jobs library"]["job1"]["JSONfileToBeEdited"] != None
        assert len(P_JSON["jobs library"]["job1"]["edits"]) > 0, P_JSON["jobs library"]["job1"]["edits"]
        assert P_JSON["jobs library"]["job2"] != None
        assert P_JSON["jobs library"]["job2"]["JSONfileToBeEdited"] != None
        assert len(P_JSON["jobs library"]["job2"]["edits"]) > 0, P_JSON["jobs library"]["job2"]["edits"]
        jobs = _JSNO_O.get_jobs()
        assert len(jobs) > 0
        assert jobs[0]["JSONfileToBeEdited"] != None
        assert len(jobs[0]["edits"]) > 0, jobs[0]["edits"]
        assert jobs[1]["JSONfileToBeEdited"] != None
        assert len(jobs[1]["edits"]) > 0, jobs[1]["edits"]
    def test_jobsJSONfileToBeEdited(self):
        _JSNO_O = ScriptedJsonEditor.JsonJobsFile()
        _JSNO_O._load(test_test_strings.jobsJSONfileToBeEdited)
        P_JSON, config = _JSNO_O._read()
        assert P_JSON["jobs library"]["jobJSONfileToBeEdited"] != None
        assert P_JSON["jobs library"]["jobJSONfileToBeEdited"]["JSONfileToBeEdited"] == "test/player.json", P_JSON["jobs library"]["jobJSONfileToBeEdited"]["JSONfileToBeEdited"]
      
    def test_jobs2base(self):
        _JSNO_O = ScriptedJsonEditor.JsonJobsFile()
        _JSNO_O._load(test_test_strings.jobs2base)
        P_JSON, config = _JSNO_O._read()
        assert P_JSON["jobs"] != None
        for j in P_JSON["jobs"]:
          assert P_JSON["jobs library"][j] != None

    def test_jobsIncludeJsonFile(self):
        # Jobs file including another JSON file
        filepath = this_path('jobs_include2libs_test.json')
        _JSNO_O = ScriptedJsonEditor.JsonJobsFile()
        P_JSON, config = _JSNO_O.read(filepath)
        assert P_JSON["jobs"] != None
        for j in P_JSON["jobs"]:
          assert P_JSON["jobs library"][j] != None

    def test_jobsConfig(self):
        # Jobs file with config specified
        filepath = this_path('jobs_test_configs.json')
        _JSNO_O = ScriptedJsonEditor.JsonJobsFile()
        P_JSON, config = _JSNO_O.read(filepath)
        assert P_JSON["jobs"] != None
        for j in P_JSON["jobs"]:
          assert P_JSON["jobs library"][j] != None
        assert config["PLAYER.JSON"] == r'Tests\player.JSON', config["PLAYER.JSON"]

if __name__ == '__main__':
    unittest.main()
  