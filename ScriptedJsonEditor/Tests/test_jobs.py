import os
import sys
import unittest

import test_test_strings

import ScriptedJsonEditor

#sys.path.insert(0, 
this_folder = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

def this_path(filename):
  return os.path.join(this_folder, filename)

class Test_test_jobs(unittest.TestCase):
    def test_read_0(self):
        filepath = this_path('no_such_file.json')
        _JSNO_O = ScriptedJsonEditor.JsonJobsFile()
        try:
          P_JSON = _JSNO_O.read(filepath)
        except ScriptedJsonEditor.JsonContentError:
          pass
    def test_read_file(self):
        filepath = this_path('jobs_test1.json')
        _JSNO_O = ScriptedJsonEditor.JsonJobsFile()
        P_JSON = _JSNO_O.read(filepath)
        assert P_JSON["job1"] != None
        assert P_JSON["job1"]["JSONfileToBeEdited"] != None
        assert len(P_JSON["job1"]["edits"]) > 0, P_JSON["job1"]["edits"]
    def test_load_JSON_str(self):
        _JSNO_O = ScriptedJsonEditor.JsonJobsFile()
        P_JSON = _JSNO_O._load(test_test_strings.jobsJSONstr1)
        assert P_JSON["job1"] != None
        assert P_JSON["job1"]["JSONfileToBeEdited"] != None
        assert len(P_JSON["job1"]["edits"]) > 0, P_JSON["job1"]["edits"]
    def test_get_jobs(self):
        _JSNO_O = ScriptedJsonEditor.JsonJobsFile()
        P_JSON = _JSNO_O._load(test_test_strings.jobsJSONstr1)
        assert P_JSON["job1"] != None
        assert P_JSON["job1"]["JSONfileToBeEdited"] != None
        assert len(P_JSON["job1"]["edits"]) > 0, P_JSON["job1"]["edits"]
        jobs = _JSNO_O.get_jobs()
        assert len(jobs) > 0
        assert jobs[0]["JSONfileToBeEdited"] != None
        assert len(jobs[0]["edits"]) > 0, jobs[0]["edits"]

    def test_load_JSON_str_2jobs(self):
        _JSNO_O = ScriptedJsonEditor.JsonJobsFile()
        P_JSON = _JSNO_O._load(test_test_strings.jobsJSONstrBadKey2)
        assert P_JSON["job1"] != None
        assert P_JSON["job1"]["JSONfileToBeEdited"] != None
        assert len(P_JSON["job1"]["edits"]) > 0, P_JSON["job1"]["edits"]
        assert P_JSON["job2"] != None
        assert P_JSON["job2"]["JSONfileToBeEdited"] != None
        assert len(P_JSON["job2"]["edits"]) > 0, P_JSON["job2"]["edits"]
    def test_get_2jobs(self):
        _JSNO_O = ScriptedJsonEditor.JsonJobsFile()
        P_JSON = _JSNO_O._load(test_test_strings.jobsJSONstrBadKey2)
        assert P_JSON["job1"] != None
        assert P_JSON["job1"]["JSONfileToBeEdited"] != None
        assert len(P_JSON["job1"]["edits"]) > 0, P_JSON["job1"]["edits"]
        assert P_JSON["job2"] != None
        assert P_JSON["job2"]["JSONfileToBeEdited"] != None
        assert len(P_JSON["job2"]["edits"]) > 0, P_JSON["job2"]["edits"]
        jobs = _JSNO_O.get_jobs()
        assert len(jobs) > 0
        assert jobs[0]["JSONfileToBeEdited"] != None
        assert len(jobs[0]["edits"]) > 0, jobs[0]["edits"]
        assert jobs[1]["JSONfileToBeEdited"] != None
        assert len(jobs[1]["edits"]) > 0, jobs[1]["edits"]
    def test_jobsJSONfileToBeEdited(self):
        _JSNO_O = ScriptedJsonEditor.JsonJobsFile()
        P_JSON = _JSNO_O._load(test_test_strings.jobsJSONfileToBeEdited)
        assert P_JSON["jobJSONfileToBeEdited"] != None
        assert P_JSON["jobJSONfileToBeEdited"]["JSONfileToBeEdited"] == "test/player.json", P_JSON["jobJSONfileToBeEdited"]["JSONfileToBeEdited"]
      


if __name__ == '__main__':
    unittest.main()
  