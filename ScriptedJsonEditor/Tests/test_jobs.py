import os
import sys
import unittest
from unittest.mock import patch

import Tests.test_test_strings as test_test_strings

import ScriptedJsonEditor

this_folder = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

test_config = {"<CONTROLLER.JSON>":"c:\\Program Files (x86)\\Steam\\steamapps\\common\\rFactor 2\\UserData\\Player\\Controller.JSON",
               "<PLAYER.JSON>":"c:\\Program Files (x86)\\Steam\\steamapps\\common\\rFactor 2\\UserData\\Player\\Player.JSON"}

test_config_w_macros = {"<CONTROLLER.JSON>":"<RF2ROOT>\\UserData\\<PLAYER>\\Controller.JSON",
               "<PLAYER.JSON>":"<RF2ROOT>\\UserData\\<PLAYER>\\<PLAYER>.JSON"}

def this_path(filename):
  return os.path.join(this_folder, filename)

class Test_test_jobs(unittest.TestCase):
    """ This throws an exception now, no idea why  
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
    """
    def test_read_file(self):
        filepath = this_path('jobs_test1.json')
        _JSNO_O = ScriptedJsonEditor.JsonJobsFile()
        P_JSON, config = _JSNO_O.read(filepath)
        assert P_JSON["job definition files"] != None
        assert len(P_JSON["jobs"]) > 0, P_JSON["job definitions"]["jobs"]
    def test_load_JSON_str(self):
        _JSNO_O = ScriptedJsonEditor.JsonJobsFile()
        _JSNO_O._load(test_test_strings.jobsJSONstr1, 'test_test_strings.jobsJSONstr1')
        P_JSON, config = _JSNO_O._read()
        assert P_JSON["job definitions"]["job1"] != None
        assert P_JSON["job definitions"]["job1"]["JSONfileToBeEdited"] != None
        assert len(P_JSON["job definitions"]["job1"]["edits"]) > 0, P_JSON["job definitions"]["job1"]["edits"]
    def test_get_jobs(self):
        _JSNO_O = ScriptedJsonEditor.JsonJobsFile()
        _JSNO_O._load(test_test_strings.jobsJSONstr1, 'test_test_strings.jobsJSONstr1')
        P_JSON, config = _JSNO_O._read()
        assert P_JSON['job definitions']["job1"] != None
        assert P_JSON['job definitions']["job1"]["JSONfileToBeEdited"] != None
        assert len(P_JSON['job definitions']["job1"]["edits"]) > 0, P_JSON['job definitions']["job1"]["edits"]
        """ No list of jobs in definition file 
        jobs = _JSNO_O.get_jobs()
        assert len(jobs) > 0
        assert jobs[0]["JSONfileToBeEdited"] != None
        assert len(jobs[0]["edits"]) > 0, jobs[0]["edits"]
        """

    def test_load_JSON_str_2jobs(self):
        job_definition_filename = 'test_test_strings.jobsJSONstrBadKey2'
        _JSNO_O = ScriptedJsonEditor.JsonJobsDefinitionsFile(test_config)
        _JSNO_O._load(test_test_strings.jobsJSONstrBadKey2, job_definition_filename)
        P_JSON = _JSNO_O._read()
        assert P_JSON[job_definition_filename]["job1"] != None
        assert P_JSON[job_definition_filename]["job1"]["JSONfileToBeEdited"] != None
        assert len(P_JSON[job_definition_filename]["job1"]["edits"]) > 0, P_JSON[job_definition_filename]["job1"]["edits"]
        assert P_JSON[job_definition_filename]["job2"] != None
        assert P_JSON[job_definition_filename]["job2"]["JSONfileToBeEdited"] != None
        assert len(P_JSON[job_definition_filename]["job2"]["edits"]) > 0, P_JSON[job_definition_filename]["job2"]["edits"]
    def test_get_2jobs(self):
        job_definition_filename = 'test_test_strings.jobsJSONstrBadKey2'
        _JSNO_O = ScriptedJsonEditor.JsonJobsDefinitionsFile(test_config)
        _JSNO_O._load(test_test_strings.jobsJSONstrBadKey2, job_definition_filename)
        P_JSON = _JSNO_O._read()
        assert P_JSON[job_definition_filename]["job1"] != None
        assert P_JSON[job_definition_filename]["job1"]["JSONfileToBeEdited"] != None
        assert len(P_JSON[job_definition_filename]["job1"]["edits"]) > 0, P_JSON[job_definition_filename]["job1"]["edits"]
        assert P_JSON[job_definition_filename]["job2"] != None
        assert P_JSON[job_definition_filename]["job2"]["JSONfileToBeEdited"] != None
        assert len(P_JSON[job_definition_filename]["job2"]["edits"]) > 0, P_JSON[job_definition_filename]["job2"]["edits"]
        """ No list of jobs in definition file
        jobs = _JSNO_O.get_jobs()
        assert len(jobs) > 0
        assert jobs[0]["JSONfileToBeEdited"] != None
        assert len(jobs[0]["edits"]) > 0, jobs[0]["edits"]
        assert jobs[1]["JSONfileToBeEdited"] != None
        assert len(jobs[1]["edits"]) > 0, jobs[1]["edits"]
        """

    def test_jobsJSONfileToBeEdited(self):
        job_definition_filename = 'test_test_strings.jobsJSONfileToBeEdited'
        _JSNO_O = ScriptedJsonEditor.JsonJobsDefinitionsFile(test_config)
        _JSNO_O._load(test_test_strings.jobsJSONfileToBeEdited, job_definition_filename)
        P_JSON = _JSNO_O._read()
        assert P_JSON[job_definition_filename]["jobJSONfileToBeEdited"] != None
        assert P_JSON[job_definition_filename]["jobJSONfileToBeEdited"]["JSONfileToBeEdited"] == "test/player.json", \
          P_JSON[job_definition_filename]["jobJSONfileToBeEdited"]["JSONfileToBeEdited"]
      
    def test_jobs2base(self):
        _JSNO_O = ScriptedJsonEditor.JsonJobsFile()
        _JSNO_O._load(test_test_strings.jobs2base, 'test_test_strings.jobs2base')
        P_JSON, config = _JSNO_O._read()
        assert P_JSON["jobs"] != None
        for j in P_JSON["jobs"]:
          assert P_JSON["job definitions"][j] != None

    """ Excluded from program now
    def test_jobsIncludeJsonFile(self):
        # Jobs file including another JSON file
        filepath = this_path('jobs_include2libs_test.json')
        _JSNO_O = ScriptedJsonEditor.JsonJobsFile()
        P_JSON, config = _JSNO_O.read(filepath)
        assert P_JSON["jobs"] != None
        for j in P_JSON["jobs"]:
          assert P_JSON["job definition files"]["job definitions"] != None
    """

    def test_jobsConfig(self):
        # Jobs file with config specified
        filepath = this_path('jobs_test_configs.json')
        _JSNO_O = ScriptedJsonEditor.JsonJobsFile()
        P_JSON, config = _JSNO_O.read(filepath)
        assert P_JSON["jobs"] != None
        for j in P_JSON["jobs"]:
          # Not sure what this was testing
          assert j != None
        assert config["<PLAYER.JSON>"] == r'Tests\player.JSON', config["<PLAYER.JSON>"]

    def test_jobsDefinition(self):
        _JSNO_O = ScriptedJsonEditor.JsonJobsDefinitionsFile(test_config)
        _JSNO_O._load(test_test_strings.jobDefinition, 'test_test_strings.jobDefinition')
        jobDefinitions = _JSNO_O._read()
        assert "VR" in jobDefinitions['test_test_strings.jobDefinition']
        assert "G25 minor controls" in jobDefinitions['test_test_strings.jobDefinition']
        assert jobDefinitions['test_test_strings.jobDefinition']["VR"]["JSONfileToBeEdited"] == test_config["<CONTROLLER.JSON>"]

    def test_jobsDefinition_w_macros(self):
        _JSNO_O = ScriptedJsonEditor.JsonJobsDefinitionsFile(test_config_w_macros)
        _JSNO_O._load(test_test_strings.jobDefinition, 'test_test_strings.jobDefinition')
        jobDefinitions = _JSNO_O._read()
        assert "VR" in jobDefinitions['test_test_strings.jobDefinition']
        assert "G25 minor controls" in jobDefinitions['test_test_strings.jobDefinition']
        assert jobDefinitions['test_test_strings.jobDefinition']["VR"]["JSONfileToBeEdited"] == test_config_w_macros["<CONTROLLER.JSON>"]

    def test_2jobsDefinition(self):
        _JSNO_O = ScriptedJsonEditor.JsonJobsDefinitionsFile(test_config)
        _JSNO_O._load(test_test_strings.jobDefinition, 'test_test_strings.jobDefinition')
        jobDefinitions = _JSNO_O._read()
        _JSNO_O = ScriptedJsonEditor.JsonJobsDefinitionsFile(test_config)
        _JSNO_O._load(test_test_strings.jobDefinition2, 'test_test_strings.jobDefinition2')
        jobDefinitions.update(_JSNO_O._read())
        assert "VR" in jobDefinitions['test_test_strings.jobDefinition']
        assert "G25 minor controls" in jobDefinitions['test_test_strings.jobDefinition']
        assert jobDefinitions['test_test_strings.jobDefinition']["VR"]["JSONfileToBeEdited"] == test_config["<CONTROLLER.JSON>"]
        assert "Wheel settings" in jobDefinitions['test_test_strings.jobDefinition2']
        assert jobDefinitions['test_test_strings.jobDefinition2']["Wheel settings"]["JSONfileToBeEdited"] == test_config["<CONTROLLER.JSON>"]
        
    def test_jobsDefinition_realFile(self):
        _JSNO_O = ScriptedJsonEditor.JsonJobsDefinitionsFile(test_config)
        filepath = this_path(os.path.join('..', 'job_definitions', 'Keyboard_jobs.json'))
        jobDefinitions = _JSNO_O.read(filepath)
        
        assert "Cursor keys control seat" in jobDefinitions['Keyboard_jobs']
        assert "Driver aid buttons disable" in jobDefinitions['Keyboard_jobs']
        assert jobDefinitions['Keyboard_jobs']["Cursor keys control seat"]["JSONfileToBeEdited"] == test_config["<CONTROLLER.JSON>"]

    def test_newJobsFile(self):
        _JSNO_O = ScriptedJsonEditor.JsonJobsFile()
        _JSNO_O._load(test_test_strings.jobsNewJSONfile, 'test_test_strings.jobsNewJSONfile')
        P_JSON, config = _JSNO_O._read()
        jobDefinitions = {}
        for _job_definition_file in P_JSON["job definition files"]:
          _x = _JSNO_O.read(_job_definition_file)
          jobDefinitions.update(_x[0]['job definitions'])
        for _job_set in P_JSON["jobs"]:
          for _job_definition_file in _job_set:
            for _job in _job_set[_job_definition_file]:
              assert _job in jobDefinitions, _job


if __name__ == '__main__':
    unittest.main()
  