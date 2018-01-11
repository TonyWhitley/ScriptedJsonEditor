import os
import unittest
from unittest.mock import patch

import ScriptedJsonEditor
import test_test_strings
import command_line

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

    def test_get_job_definitions(self):
        config = {"<CONTROLLER.JSON>":"c:\\Program Files (x86)\\Steam\\steamapps\\common\\rFactor 2\\UserData\\Player\\Controller.JSON"}
        _jsonJob = ScriptedJsonEditor.JsonJobsDefinitionsFile(config)
        P_JSON = _jsonJob._load(command_line.JOB_DEFINITIONS_FILE_HELP_STR, 'command_line.JOB_DEFINITIONS_FILE_HELP_STR')
        assert P_JSON["job definitions"]["Letterboxing off"] != None
        assert P_JSON["job definitions"]["Letterboxing off"]["JSONfileToBeEdited"] != None
        assert len(P_JSON["job definitions"]["Letterboxing off"]["edits"]) > 0, P_JSON["job definitions"]["Letterboxing off"]["edits"]
        """
        No longer in the same file
        jobs = _jsonJob.get_jobs()
        assert len(jobs) > 0
        assert jobs[0]["JSONfileToBeEdited"] != None
        assert len(jobs[0]["edits"]) > 0, jobs[0]["edits"]
        """

    def test_run_job(self):
        _jsonJob = ScriptedJsonEditor.JsonJobsFile()
        _jsonJob._load(command_line.JOBS_FILE_HELP_STR, 'command_line.JOBS_FILE_HELP_STR')
        P_JSON, config = _jsonJob._read()

        _jsonJobDefs = ScriptedJsonEditor.JsonJobsDefinitionsFile(config)
        _jsonJobDefs._load(command_line.JOB_DEFINITIONS_FILE_HELP_STR, 'test_test_strings.keyboard_jobs_json_file')
        _jsonJobDefs._read()

        """
        assert P_JSON["job definitions"]["Letterboxing off"] != None
        assert P_JSON["job definitions"]["Letterboxing off"]["JSONfileToBeEdited"] != None
        assert len(P_JSON["job definitions"]["Letterboxing off"]["edits"]) > 0, P_JSON["job definitions"]["Letterboxing off"]["edits"]
        """
        jobs = _jsonJob.get_jobs()
        assert len(jobs) > 0
        """
        No longer in the same file
        assert jobs[0]["JSONfileToBeEdited"] != None
        assert len(jobs[0]["edits"]) > 0, jobs[0]["edits"]
        """
        
        for i, job in enumerate(jobs):
          _j = ScriptedJsonEditor.Job(job, config)
          #   read the file to be edited
          P_JSON = _j._load(test_test_strings.playerJSONstr, 'test_test_strings.playerJSONstr')
          assert P_JSON["Graphic Options"] != None
          assert P_JSON["Graphic Options"]["Allow HUD in cockpit"] != None
          assert P_JSON["Graphic Options"]["Allow HUD in cockpit"], P_JSON["Graphic Options"]["Allow HUD in cockpit"]

          # before job
          assert _j._get_value("Graphic Options", "Allow Letterboxing") == True, P_JSON._get_value("Graphic Options", "Allow Letterboxing")

          #   do the edits
          _j.run_edits()

          if i == 0:
            assert _j._get_value("Graphic Options", "Allow Letterboxing") == False, P_JSON._get_value("Graphic Options", "Allow Letterboxing")
          else:
            assert _j._get_value("Graphic Options", "Automap") == 3, P_JSON._get_value("Graphic Options", "Automap")
        
    """ this is a job description file now
    @patch('ScriptedJsonEditor.print', create=True)   # Mock the print call in ScriptedJsonEditor()
    def test_run_2jobs(self, print_):                 # Note added , print_ to mock print()
        # Expect job2 to fail
        _jsonJob = ScriptedJsonEditor.JsonJobsFile()
        _jsonJob._load(test_test_strings.jobsJSONstrBadKey2, 'test_test_strings.jobsJSONstrBadKey2')
        P_JSON, config = _jsonJob._read()
        assert P_JSON["job definitions"]["job1"] != None
        assert P_JSON["job definitions"]["job1"]["JSONfileToBeEdited"] != None
        assert len(P_JSON["job definitions"]["job1"]["edits"]) > 0, P_JSON["job definitions"]["job1"]["edits"]
        jobs = _jsonJob.get_jobs()
        assert len(jobs) > 0
        assert jobs[0]["JSONfileToBeEdited"] != None
        assert len(jobs[0]["edits"]) > 0, jobs[0]["edits"]
        
        # job 1
        job = jobs[0]
        _j = ScriptedJsonEditor.Job(job, config)
        #   read the file to be edited
        P_JSON = _j._load(test_test_strings.playerJSONstr, 'test_test_strings.playerJSONstr')
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
        _j = ScriptedJsonEditor.Job(job, config)
        #   read the file to be edited
        P_JSON = _j._load(test_test_strings.playerJSONstr, 'test_test_strings.playerJSONstr')

        # before job 2
        assert _j._get_value("Graphic Options", "Shadows") == 0, _j._get_value("Graphic Options", "Shadows")

        try:
          #   do the edits
          _j.run_edits()
        except KeyError:
          # That's expected
          assert _j._get_value("Graphic Options", "Shadow Blur") == 4, _j._get_value("Graphic Options", "Shadow Blur")
            
        assert _j._get_value("Graphic Options", "Shadows") == 1, _j._get_value("Graphic Options", "Shadows")
      """
        
if __name__ == '__main__':
    unittest.main()
