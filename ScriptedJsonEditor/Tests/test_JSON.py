import os
import unittest

import ScriptedJsonEditor
import test_test_strings

filepath = r'c:\Program Files (x86)\Steam\steamapps\common\rFactor 2\UserData\player\player.json'



class Test_test_JSON(unittest.TestCase):
    def test_readJsonFile(self):
        if os.path.exists(filepath):
          _JSNO_O = ScriptedJsonEditor.JsonFile()
          P_JSON = _JSNO_O.read(filepath)
          _filepath = filepath + '.mostlySame'
          _JSNO_O.write(_filepath)

    def test_editJson(self):
        if os.path.exists(filepath):
          _JSNO_O = ScriptedJsonEditor.JsonFile()
          P_JSON = _JSNO_O.read(filepath)
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
        _jsonJob = ScriptedJsonEditor.JsonFile()
        P_JSON = _jsonJob._load(test_test_strings.jobsJSONhelpStr)
        assert P_JSON["job1"] != None
        assert P_JSON["job1"]["JSONfileToBeEdited"] != None
        assert len(P_JSON["job1"]["edits"]) > 0, P_JSON["job1"]["edits"]
        jobs = _jsonJob.get_jobs()
        assert len(jobs) > 0
        assert jobs[0]["JSONfileToBeEdited"] != None
        assert len(jobs[0]["edits"]) > 0, jobs[0]["edits"]

    def test_run_job(self):
        _jsonJob = ScriptedJsonEditor.JsonFile()
        P_JSON = _jsonJob._load(test_test_strings.jobsJSONhelpStr)
        assert P_JSON["job1"] != None
        assert P_JSON["job1"]["JSONfileToBeEdited"] != None
        assert len(P_JSON["job1"]["edits"]) > 0, P_JSON["job1"]["edits"]
        jobs = _jsonJob.get_jobs()
        assert len(jobs) > 0
        assert jobs[0]["JSONfileToBeEdited"] != None
        assert len(jobs[0]["edits"]) > 0, jobs[0]["edits"]
        
        _JSNO_O = ScriptedJsonEditor.JsonFile()
        P_JSON = _JSNO_O._load(test_test_strings.playerJSONstr)
        assert P_JSON["Graphic Options"] != None
        assert P_JSON["Graphic Options"]["Allow HUD in cockpit"] != None
        assert P_JSON["Graphic Options"]["Allow HUD in cockpit"], P_JSON["Graphic Options"]["Allow HUD in cockpit"]

        # before job
        assert _JSNO_O._get_value("Graphic Options", "Allow Letterboxing") == True, _JSNO_O._get_value("Graphic Options", "Allow Letterboxing")

        for job in jobs:
          _JSNO_O.run_edits(job)

        assert _JSNO_O._get_value("Graphic Options", "Allow Letterboxing") == False, _JSNO_O._get_value("Graphic Options", "Allow Letterboxing")
        
    def test_run_2jobs(self):
        # Expect job2 to fail
        _jsonJob = ScriptedJsonEditor.JsonFile()
        P_JSON = _jsonJob._load(test_test_strings.jobsJSONstrBadKey2)
        assert P_JSON["job1"] != None
        assert P_JSON["job1"]["JSONfileToBeEdited"] != None
        assert len(P_JSON["job1"]["edits"]) > 0, P_JSON["job1"]["edits"]
        jobs = _jsonJob.get_jobs()
        assert len(jobs) > 0
        assert jobs[0]["JSONfileToBeEdited"] != None
        assert len(jobs[0]["edits"]) > 0, jobs[0]["edits"]
        
        _JSNO_O = ScriptedJsonEditor.JsonFile()
        P_JSON = _JSNO_O._load(test_test_strings.playerJSONstr)
        assert P_JSON["Graphic Options"] != None
        assert P_JSON["Graphic Options"]["Allow HUD in cockpit"] != None
        assert P_JSON["Graphic Options"]["Allow HUD in cockpit"], P_JSON["Graphic Options"]["Allow HUD in cockpit"]

        # before job 1
        assert _JSNO_O._get_value("Graphic Options", "Track Detail") == 0, _JSNO_O._get_value("Graphic Options", "Track Detail")
        # before job 2
        assert _JSNO_O._get_value("Graphic Options", "Shadows") == 0, _JSNO_O._get_value("Graphic Options", "Shadows")

        for job in jobs:
          try:
            _JSNO_O.run_edits(job)
          except KeyError:
            # That's expected
            assert _JSNO_O._get_value("Graphic Options", "Shadow Blur") == 4, _JSNO_O._get_value("Graphic Options", "Shadow Blur")
            
        # job1 values will change, but main() will not write the new file
        assert _JSNO_O._get_value("Graphic Options", "Track Detail") == 1, _JSNO_O._get_value("Graphic Options", "Track Detail")
        assert _JSNO_O._get_value("Graphic Options", "Shadows") == 1, _JSNO_O._get_value("Graphic Options", "Shadows")
        
if __name__ == '__main__':
    unittest.main()
