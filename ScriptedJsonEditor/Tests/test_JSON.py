import os
import unittest

import ScriptedJsonEditor
import test_test_strings

filepath = r'player.json'



class Test_test_JSON(unittest.TestCase):
    def test_readJsonFile(self):
        if os.path.exists(filepath):
          _JSNO_O = ScriptedJsonEditor.JsonRfactorFile()
          _JSNO_O.read(filepath)
          _filepath = filepath + '.mostlySame'
          _JSNO_O.write(_filepath)

    def test_editJson(self):
        if os.path.exists(filepath):
          _JSNO_O = ScriptedJsonEditor.JsonRfactorFile()
          _JSNO_O.read(filepath)
          ##################################
          # change values as required
          ##################################
          for key, item, newValue in test_test_strings.edits:
            try:
              _JSNO_O.edit(key, item, newValue)
            except KeyError:  # we're expecting one error
              assert key == 'GraphicOptions', key
  
          _filepath = filepath + '.edited'
          _JSNO_O.write(_filepath)

    def test_get_jobs(self):
        _jsonJob = ScriptedJsonEditor.JsonJobsFile()
        P_JSON = _jsonJob._load(test_test_strings.JOBS_JSON_HELP_STR)
        assert P_JSON["job1"] != None
        assert P_JSON["job1"]["JSONfileToBeEdited"] != None
        assert len(P_JSON["job1"]["edits"]) > 0, P_JSON["job1"]["edits"]
        jobs = _jsonJob.get_jobs()
        assert len(jobs) > 0
        assert jobs[0]["JSONfileToBeEdited"] != None
        assert len(jobs[0]["edits"]) > 0, jobs[0]["edits"]

    def test_run_job(self):
        _jsonJob = ScriptedJsonEditor.JsonJobsFile()
        P_JSON = _jsonJob._load(test_test_strings.JOBS_JSON_HELP_STR)
        assert P_JSON["job1"] != None
        assert P_JSON["job1"]["JSONfileToBeEdited"] != None
        assert len(P_JSON["job1"]["edits"]) > 0, P_JSON["job1"]["edits"]
        jobs = _jsonJob.get_jobs()
        assert len(jobs) > 0
        assert jobs[0]["JSONfileToBeEdited"] != None
        assert len(jobs[0]["edits"]) > 0, jobs[0]["edits"]
        
        for job in jobs:
          _j = ScriptedJsonEditor.Job(job)
          #   read the file to be edited
          P_JSON = _j._load(test_test_strings.playerJSONstr)
          assert P_JSON["Graphic Options"] != None
          assert P_JSON["Graphic Options"]["Allow HUD in cockpit"] != None
          assert P_JSON["Graphic Options"]["Allow HUD in cockpit"], P_JSON["Graphic Options"]["Allow HUD in cockpit"]

          # before job
          assert _j._get_value("Graphic Options", "Allow Letterboxing") == True, _JSNO_O._get_value("Graphic Options", "Allow Letterboxing")

          #   do the edits
          _j.run_edits()

          assert _j._get_value("Graphic Options", "Allow Letterboxing") == False, _JSNO_O._get_value("Graphic Options", "Allow Letterboxing")
        
    def test_run_2jobs(self):
        # Expect job2 to fail
        _jsonJob = ScriptedJsonEditor.JsonJobsFile()
        P_JSON = _jsonJob._load(test_test_strings.jobsJSONstrBadKey2)
        assert P_JSON["job1"] != None
        assert P_JSON["job1"]["JSONfileToBeEdited"] != None
        assert len(P_JSON["job1"]["edits"]) > 0, P_JSON["job1"]["edits"]
        jobs = _jsonJob.get_jobs()
        assert len(jobs) > 0
        assert jobs[0]["JSONfileToBeEdited"] != None
        assert len(jobs[0]["edits"]) > 0, jobs[0]["edits"]
        
        # job 1
        job = jobs[0]
        _j = ScriptedJsonEditor.Job(job)
        #   read the file to be edited
        P_JSON = _j._load(test_test_strings.playerJSONstr)
        assert P_JSON["Graphic Options"] != None
        assert P_JSON["Graphic Options"]["Allow HUD in cockpit"] != None
        assert P_JSON["Graphic Options"]["Allow HUD in cockpit"], P_JSON["Graphic Options"]["Allow HUD in cockpit"]

        # before job 1
        assert _j._get_value("Graphic Options", "Track Detail") == 0, _j._get_value("Graphic Options", "Track Detail")
        #   do the edits
        _j.run_edits()
        assert _j._get_value("Graphic Options", "Track Detail") == 1, _j._get_value("Graphic Options", "Track Detail")

        # job 2
        job = jobs[1]
        _j = ScriptedJsonEditor.Job(job)
        #   read the file to be edited
        P_JSON = _j._load(test_test_strings.playerJSONstr)

        # before job 2
        assert _j._get_value("Graphic Options", "Shadows") == 0, _j._get_value("Graphic Options", "Shadows")

        try:
          #   do the edits
          _j.run_edits()
        except KeyError:
          # That's expected
          assert _j._get_value("Graphic Options", "Shadow Blur") == 4, _j._get_value("Graphic Options", "Shadow Blur")
            
        assert _j._get_value("Graphic Options", "Shadows") == 1, _j._get_value("Graphic Options", "Shadows")
        
if __name__ == '__main__':
    unittest.main()
