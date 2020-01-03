import os
import unittest
from unittest.mock import patch

import ScriptedJsonEditor
import Tests.test_test_strings as test_test_strings
import command_line

filepath = r'player.json'

# Edits to command_line.JOBS_FILE_HELP_STR to produce
# EDITED_JOBS_FILE_HELP_STR below
EDITS = {
    "<PLAYER.JSON>": "c:\\Program Files (x86)\\Steam\\steamapps\\common\\rFactor 2\\UserData\\Player\\EDITED_player.JSON",
    "job definition files": [
        "job_definitions\\Game_jobs.json"
    ],
    "jobs": [
        {
            "Game_jobs": [
                "DRIVING AIDS",
                "Flags off"
            ]
        }
    ]
}

EDITED_JOBS_FILE_HELP_STR = r"""
{
  "<PLAYER.JSON>": "c:\\Program Files (x86)\\Steam\\steamapps\\common\\rFactor 2\\UserData\\Player\\EDITED_player.JSON",
  "jobs file format": 6,
  "job definition files": [
    "job_definitions\\Game_jobs.json"
  ],
  "jobs": [
    {
      "Game_jobs": [
        "DRIVING AIDS",
        "Flags off"
      ]
    }
  ]
}
"""


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
        config = {
            "<CONTROLLER.JSON>": "c:\\Program Files (x86)\\Steam\\steamapps\\common\\rFactor 2\\UserData\\Player\\Controller.JSON"}
        _jsonJob = ScriptedJsonEditor.JsonJobsDefinitionsFile(config)
        P_JSON = _jsonJob._load(
            command_line.JOB_DEFINITIONS_FILE_HELP_STR,
            'command_line.JOB_DEFINITIONS_FILE_HELP_STR')
        assert P_JSON["job definitions"]["Letterboxing off"] is not None
        assert P_JSON["job definitions"]["Letterboxing off"]["JSONfileToBeEdited"] is not None
        assert len(P_JSON["job definitions"]["Letterboxing off"]["edits"]
                   ) > 0, P_JSON["job definitions"]["Letterboxing off"]["edits"]
        """
        No longer in the same file
        jobs = _jsonJob.get_jobs()
        assert len(jobs) > 0
        assert jobs[0]["JSONfileToBeEdited"] != None
        assert len(jobs[0]["edits"]) > 0, jobs[0]["edits"]
        """

    def test_run_job(self):
        _jsonJob = ScriptedJsonEditor.JsonJobsFile()
        _jsonJob._load(
            command_line.JOBS_FILE_HELP_STR,
            'command_line.JOBS_FILE_HELP_STR')
        P_JSON, config = _jsonJob._read()

        _jsonJobDefs = ScriptedJsonEditor.JsonJobsDefinitionsFile(config)
        _jsonJobDefs._load(
            command_line.JOB_DEFINITIONS_FILE_HELP_STR,
            'test_test_strings.keyboard_jobs_json_file')
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
            P_JSON = _j._load(
                test_test_strings.playerJSONstr,
                'test_test_strings.playerJSONstr')
            assert P_JSON["Graphic Options"] is not None
            assert P_JSON["Graphic Options"]["Allow HUD in cockpit"] is not None
            assert P_JSON["Graphic Options"]["Allow HUD in cockpit"], P_JSON["Graphic Options"]["Allow HUD in cockpit"]

            # before job
            assert _j._get_value(
                "Graphic Options", "Allow Letterboxing"), _j._get_value(
                "Graphic Options", "Allow Letterboxing")

            #   do the edits
            _j.run_edits()

            if i == 0:
                assert _j._get_value(
                    "Graphic Options", "Allow Letterboxing") == False, _j._get_value(
                    "Graphic Options", "Allow Letterboxing")
            else:
                assert _j._get_value(
                    "Graphic Options", "Automap") == 2, _j._get_value(
                    "Graphic Options", "Automap")

    def test_edit_job_file(self):
        _jsonJob = ScriptedJsonEditor.JsonJobsFile()
        _jsonJob._load(
            command_line.JOBS_FILE_HELP_STR,
            'command_line.JOBS_FILE_HELP_STR')
        P_JSON, __ = _jsonJob._read()
        # Copy JOBS_FILE_HELP_STR and edit it - or just use EDITED_JOBS_FILE_HELP_STR
        # Run edit_job_file
        # _write it to a string??
        # compare to the edited JOBS_FILE_HELP_STR
        _jsonJob._edit_job_file(EDITS)
        # _jsonJob._write()
        P_JSON_edited, __ = _jsonJob._read()

        _jsonJobTest = ScriptedJsonEditor.JsonJobsFile()
        _jsonJobTest._load(
            EDITED_JOBS_FILE_HELP_STR,
            'EDITED_JOBS_FILE_HELP_STR')
        P_JSON_TEST_STR, __ = _jsonJobTest._read()
        self.assertEqual(P_JSON_edited, P_JSON_TEST_STR)


if __name__ == '__main__':
    unittest.main()
