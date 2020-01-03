""" Test strings used by test functions """

from command_line import JOBS_FILE_HELP_STR, JOB_DEFINITIONS_FILE_HELP_STR
import json
import os
import sys
import unittest

sys.path.insert(
    0, os.path.abspath(
        os.path.dirname(
            os.path.dirname(
                os.path.realpath(__file__)))))


valid_JSON_strings = [JOBS_FILE_HELP_STR]
valid_JSON_strings.append(JOB_DEFINITIONS_FILE_HELP_STR)

edits = [
    # General graphics
    ("Graphic Options", "Track Detail", 1),  # "0=Low 1=Medium 2=High 3=Full"
    ("Graphic Options", "Player Detail", 1),
    ("Graphic Options", "Opponent Detail", 1),
    ("Graphic Options", "Texture Detail", 1),
    # "0, bilinear, 1, trilinear, 2, X2 AF, 3, X4 AF, 4, X8 AF, 5, X16 AF"
    ("Graphic Options", "Texture Filter", 4),

    ("Graphic Options", "Shadows", 1),
    # "0=Off, 1=Fast, 2=Optimal, 3=Quality"
    ("Graphic Options", "Shadow Blur", 0),
    # "0=Off, 1=Cheap soft edges, 2=Depth buffered soft edges"
    ("Graphic Options", "Soft Particles", 1),
    ("Graphic Options", "Rain FX Quality", 1),
    ("Graphic Options", "Road Reflections", 2),  # "Off/Low/High"
    ("Graphic Options", "Environment Reflections", 1),  # "Off/Low/High"

    # VR-specific graphics
    ("Graphic Options", "Car Vibration Mult1", 0),
    ("Graphic Options", "Car Vibration Mult2", 0),
    ("Graphic Options", "Cockpit Vibration Mult1", 0),
    ("Graphic Options", "Cockpit Vibration Mult2", 0),

    ("Graphic Options", "Look Roll Angle", 0),
    ("Graphic Options", "Head Physics", 0),
    ("Graphic Options", "Exaggerate Yaw", 0),

    ("Graphic Options", "Rearview_Back_Clip", 30),
    ("Graphic Options", "Garage Detail", 0.01),
    ("Graphic Options", "Max Headlights", 20),
    ("GraphicOptions", "Max Headlights", 20),

]

playerJSONstr = r"""
{
    "Graphic Options":{
                            "Allow HUD in cockpit":true,
                            "Allow Letterboxing":true,
                            "Allow Letterboxing#":"whether we allow letterboxing (during replays, for example)",
                            "Max Headlights": 255,
                            "Always Rebuild Collision":false,
                            "Always Rebuild Collision#":"Build collision database everytime tracks are loaded (for development purposes)",
                            "Any Camera HUD":true,
                            "Any Camera HUD#":"whether to show the HUD from any camera (in particular, tracksides)",
                            "Auto Detail Framerate":0,
                            "Auto Detail Framerate#":"Details and visible vehicles will be automatically reduced (by up to half) if framerate is under this threshold (0 to disable)",
                            "Automap":3,
                            "Automap#":"0=off 1=race-only 2=non-race-only 3=all sessions",
                            "Backfire Anim Speed":30,
                            "Box Outline":16711680,
                            "Box Outline#":"whether to draw box on ground around pitstall and grid location when necessary; -1=off, 0-16777215=RGB color",
                            "Broadcast Overlay":0,
                            "Car Vibration Mult1":0,
                            "Car Vibration Mult1#":"Primary engine vibration multiplier affects position of cameras attached directly to the car",
                            "Car Vibration Mult2":0,
                            "Car Vibration Mult2#":"Secondary engine vibration multiplier affects orientation of cameras attached directly to the car",
		                        "Shadow Blur": 4,
		                        "Shadow Blur#": "0=Off, 1=Fast, 2=Optimal, 3=Quality",
                            "Texture Filter": 4,
                            "Texture Filter#": "0, bilinear, 1, trilinear, 2, X2 AF, 3, X4 AF, 4, X8 AF, 5, X16 AF",
                            "Track Detail": 0,
		                        "Track Detail#": "0=Low 1=Medium 2=High 3=Full",
                            "Shadows": 0,
		                        "Shadows#": "0=Low 1=Medium 2=High 3=Full"
  }
}
"""
valid_JSON_strings.append(playerJSONstr)

jobsJSONstr1 = r"""
{"jobs": ["job1"],
"#Only that list of jobs will be performed": 0,
"#Not all jobs in the file will necessarily be run": 0,
"jobs file format": 6,
"job definitions":{
  "job1":
	  {
	  "JSONfileToBeEdited": "tests/player.json",
    "skip keys with # in them": true,
    "# keys with # in them are used as comments, don't change the values": 0,
    "rFactor escape slash": true,
    "# rFactor 2 escapes /. Also remove space after the :": 0,

	  "edits": {
		  "Graphic Options":{
		  "Track Detail": 1,
		  "Track Detail#": "0=Low 1=Medium 2=High 3=Full",
		  "Texture Filter": 4,
		  "Texture Filter#": "0, bilinear, 1, trilinear, 2, X2 AF, 3, X4 AF, 4, X8 AF, 5, X16 AF"
		  }
	    }
	  }
  }
}
"""
valid_JSON_strings.append(jobsJSONstr1)

# Valid JSON but key name in job2 is wrong
jobsJSONstrBadKey2 = r"""
{"jobs": ["job1", "job2"],
"jobs file format": 6,
"job definitions":{
  "job1":
	  {
	  "JSONfileToBeEdited": "tests/player.json",
    "skip keys with # in them": true,
    "# keys with # in them are used as comments, don't change the values": 0,
    "rFactor escape slash": true,
    "# rFactor 2 escapes /. Also remove space after the :": 0,

	  "edits": {
		  "Graphic Options":{
		  "Track Detail": 1,
		  "Track Detail#": "0=Low 1=Medium 2=High 3=Full",
		  "Texture Filter": 4,
		  "Texture Filter#": "0, bilinear, 1, trilinear, 2, X2 AF, 3, X4 AF, 4, X8 AF, 5, X16 AF"
		  }
	    }
	  },
  "job2":
	  {
	  "JSONfileToBeEdited": "tests/player.json",
    "skip keys with # in them": true,
    "# keys with # in them are used as comments, don't change the values": 0,
    "rFactor escape slash": true,
    "# rFactor 2 escapes /. Also remove space after the :": 0,

	  "edits": {
		  "Graphic Options":{
		  "Shadows": 1,
		  "Shadows#": "0=Low 1=Medium 2=High 3=Full",
		  "Shadow Blue": 4,
		  "Shadow Blur#": "0=Off, 1=Fast, 2=Optimal, 3=Quality"
		  }
	    }
	  }
  }
}
"""
valid_JSON_strings.append(jobsJSONstrBadKey2)

# Valid JSON but key name is wrong
jobsJSONstrBadKey = r"""
{"jobs": ["job1"],
"jobs file format": 6,
"job definitions":{
  "job1":
	  {
	  "JSONfileToBeEdited": "tests/player.json",
    "skip keys with # in them": true,
    "# keys with # in them are used as comments, don't change the values": 0,
    "rFactor escape slash": true,
    "# rFactor 2 escapes /. Also remove space after the :": 0,

	  "edits": {
		  "Graphic Options":{
                              "Allow Letterboxing":false,
                              "Allow Letterboxing#":"whether we allow letterboxing (during replays, for example)",
                              "Auto Detail Framerate":50,
                              "Auto Detail Framerate#":"Details and visible vehicles will be automatically reduced (by up to half) if framerate is under this threshold (0 to disable)",
                              "Max Headlights": 20,
                              "MaxHeadlights": 20,
                              "Key above misspelled#": 0
		                    }
	            }
	  }
  }
}
"""
valid_JSON_strings.append(jobsJSONstrBadKey)

# Valid JSON, check JSONfileToBeEdited
jobsJSONfileToBeEdited = r"""
{"jobs": ["jobJSONfileToBeEdited"],
"jobs file format": 6,
"job definitions":{
  "jobJSONfileToBeEdited":
	  {
	  "JSONfileToBeEdited": "test/player.json",
    "skip keys with # in them": true,
    "# keys with # in them are used as comments, don't change the values": 0,
    "rFactor escape slash": true,
    "# rFactor 2 escapes /. Also remove space after the :": 0,

	  "edits": {
		  "Graphic Options":{
                              "Allow Letterboxing":false
		                    }
	            }
	  }
  }
}
"""
valid_JSON_strings.append(jobsJSONfileToBeEdited)

# Type 2 jobs file
jobs2base = r"""
{ "jobs": ["job1", "fred", "harry"],
"jobs file format": 6,
"job definitions":{
  "job1": {},
  "job2": {},
  "fred": {},
  "harry": {},
  "job3": {}
  }
}
"""
valid_JSON_strings.append(jobs2base)

jobDefinition = r"""
{
"job definitions":{
  "VR": {
    "JSONfileToBeEdited": "<CONTROLLER.JSON>",
    "edits": {
      "Input": {
        "#Tooltip: Left wheel button is Esc": 0,
        "Control - Alternate Esc": [
          1,
          39
        ],
        "#Tooltip: Right wheel button is re-centres head": 0,
        "Control - VR :Re-Center head position": [
          1,
          38
        ],
        "#Tooltip: Disable look left/right": 0,
        "Control - Look Left": [
          0,
          89
        ],
        "Control - Look Right": [
          0,
          89
        ]
      }
    }
  },
  "G25 minor controls": {
    "JSONfileToBeEdited": "<CONTROLLER.JSON>",
    "edits": {
       "Input": {
         "Control - Headlights": [
           1,
           49
         ],
         "Control - Reset Force Feedback": [
           1,
           34
         ]
       }
      }
    }
  }
}
"""
valid_JSON_strings.append(jobDefinition)

jobDefinition2 = r"""
{
  "job definitions": {
    "Wheel settings": {
      "JSONfileToBeEdited": "c:\\Program Files (x86)\\Steam\\steamapps\\common\\rFactor 2\\UserData\\Player\\Controller.JSON",
      "# Note: JSONfileToBeEdited .JSON is case-sensitive": 0,
      "skip keys with # in them": true,
      "# keys with # in them are used as comments, don't change the values": 0,
      "rFactor escape slash": true,
      "# rFactor 2 escapes /. Also remove space after the :": 0,
      "edits": {
        "Force Feedback": {
          "Steering torque filter": 0,
          "Steering torque filter#": "Number of old samples to use to filter torque from vehicle's steering column (0-32, note that higher values increase effective latency)",
          "Steering torque minimum": 0.12,
          "Steering torque minimum#": "Minimum torque to apply in either direction to overcome steering wheel's 'FFB deadzone' caused by friction"
        },
        "General Controls": {
          "Steering Wheel Range": 900,
          "Steering Wheel Range#": "Degrees of steering wheel rotation, both visual and physical (if available)"
        }
      }
    },
    "Cursor keys control seat": {
      "JSONfileToBeEdited": "c:\\Program Files (x86)\\Steam\\steamapps\\common\\rFactor 2\\UserData\\Player\\Controller.JSON",
      "# Note: JSONfileToBeEdited .JSON is case-sensitive": 0,
      "skip keys with # in them": true,
      "# keys with # in them are used as comments, don't change the values": 0,
      "rFactor escape slash": true,
      "# rFactor 2 escapes /. Also remove space after the :": 0,
      "edits": {
        "Input": {
          "#Tooltip: Cursor keys control seat": 0,
          "Control - Adjust Seat Aft": [
            0,
            203
          ],
          "Control - Adjust Seat Down": [
            0,
            208
          ],
          "Control - Adjust Seat Fore": [
            0,
            205
          ],
          "Control - Adjust Seat Up": [
            0,
            200
          ]
        }
      }
    }
  }
}
"""
valid_JSON_strings.append(jobDefinition2)

jobsNewJSONfile = r"""
{
  "<CONTROLLER.JSON>": "c:\\Program Files (x86)\\Steam\\steamapps\\common\\rFactor 2\\UserData\\Player\\Controller.JSON",
  "jobs file format": 6,
  "job definition files": [
    "job_definitions\\Keyboard_jobs.json"
  ],
  "jobs": [
    {
      "Keyboard_jobs": [
        "Driver aid buttons disable",
        "Cursor keys control seat"
      ]
    }
  ]
}
"""
valid_JSON_strings.append(jobsNewJSONfile)

# Contents of jobs\keyboard_jobs.json
keyboard_jobs_json_file = r"""
{
  "# Keyboard - job definitions file for ScriptedJsonEditor": 0,
  "# V1.0.0": 0,
  "# Note: any key with a # is a comment": 0,
  "jobs file format": 6,
  "job definitions": {
    "Cursor keys control seat": {
      "JSONfileToBeEdited": "<CONTROLLER.JSON>",
      "edits": {
        "Input": {
          "#Tooltip: Cursor keys control seat": 0,
          "Control - Adjust Seat Aft": [
            0,
            203
          ],
          "Control - Adjust Seat Down": [
            0,
            208
          ],
          "Control - Adjust Seat Fore": [
            0,
            205
          ],
          "Control - Adjust Seat Up": [
            0,
            200
          ]
        }
      }
    },
    "Driver aid buttons disable": {
      "JSONfileToBeEdited": "<CONTROLLER.JSON>",
      "edits": {
        "Input": {
          "Control - Anti-lock Brakes": [
            0,
            89
          ],
          "Control - Auto Clutch": [
            0,
            89
          ],
          "Control - Auto Pit Lane": [
            0,
            89
          ],
          "Control - Auto Shifting": [
            0,
            89
          ],
          "Control - Braking Help": [
            0,
            89
          ],
          "Control - Opposite Lock": [
            0,
            89
          ],
          "Control - Spin Recovery": [
            0,
            89
          ],
          "Control - Stability Control": [
            0,
            89
          ],
          "Control - Steering Help": [
            0,
            89
          ],
          "Control - Traction Control": [
            0,
            89
          ]
        }
      }
    }
  }
}
"""
valid_JSON_strings.append(keyboard_jobs_json_file)

jobsBadJSONstr = r"""
{"job1":
	{
	"JSONfileToBeEdited": "tests/player.json",
  "skip keys with # in them": true,
  "# keys with # in them are used as comments, don't change the values": 0,
  "rFactor escape slash": true,
  "# rFactor 2 escapes /. Also remove space after the :": 0,

	"edits": {
		"Graphic Options":{
                            "Allow Letterboxing":false
                            "Missed , above"#: 0,
                            "Allow Letterboxing#":"whether we allow letterboxing (during replays, for example)",
                            "Auto Detail Framerate":50,
                            "Auto Detail Framerate#":"Details and visible vehicles will be automatically reduced (by up to half) if framerate is under this threshold (0 to disable)"
		                  }
	          }
	}
}
"""
invalid_JSON_strings = [jobsBadJSONstr]


class Test_test_test_strings(unittest.TestCase):
    def test_valid_JSON_strings(self):
        for json_str in valid_JSON_strings:
            try:
                json_dict = json.loads(json_str)
            except ValueError:
                assert False, 'JSON string content error'

    def test_invalid_JSON_strings(self):
        for json_str in invalid_JSON_strings:
            try:
                json_dict = json.loads(json_str)
                assert True, 'JSON string content error expected but didn\'t happen'
            except ValueError:
                pass  # Error is expected


if __name__ == '__main__':
    unittest.main()
