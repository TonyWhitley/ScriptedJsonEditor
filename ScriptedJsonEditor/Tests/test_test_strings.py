""" Test strings used by test functions """

import json
import unittest

edits = [
    # General graphics
    ("Graphic Options", "Track Detail", 1),  # "0=Low 1=Medium 2=High 3=Full"
    ("Graphic Options", "Player Detail", 1),
    ("Graphic Options", "Opponent Detail", 1),
    ("Graphic Options", "Texture Detail", 1),
    ("Graphic Options", "Texture Filter", 4),  # "0, bilinear, 1, trilinear, 2, X2 AF, 3, X4 AF, 4, X8 AF, 5, X16 AF"

    ("Graphic Options", "Shadows", 1),
    ("Graphic Options", "Shadow Blur", 0),	# "0=Off, 1=Fast, 2=Optimal, 3=Quality"
    ("Graphic Options", "Soft Particles", 1),  # "0=Off, 1=Cheap soft edges, 2=Depth buffered soft edges"
    ("Graphic Options", "Rain FX Quality", 1), # 
    ("Graphic Options", "Road Reflections", 2), # "Off/Low/High"
    ("Graphic Options", "Environment Reflections", 1), # "Off/Low/High"
  
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
valid_JSON_strings = [playerJSONstr]

jobsJSONstr = r"""
{"job1":
	{
	"filepath": "c:\\Program Files (x86)\\Steam\\steamapps\\common\\rFactor 2\\UserData\\player\\player.json",

	"edits": {
		"Graphic Options":{
                            "Allow Letterboxing":false,
                            "Allow Letterboxing#":"whether we allow letterboxing (during replays, for example)",
                            "Auto Detail Framerate":50,
                            "Auto Detail Framerate#":"Details and visible vehicles will be automatically reduced (by up to half) if framerate is under this threshold (0 to disable)"
		                  }
	          }
	}
}
"""
valid_JSON_strings.append(jobsJSONstr)

jobsJSONstr1 = r"""
{"job1":
	{
	"filepath": "c:\\Program Files (x86)\\Steam\\steamapps\\common\\rFactor 2\\UserData\\player\\player.json",

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
"""
valid_JSON_strings.append(jobsJSONstr1)

# Valid JSON but key name in job2 is wrong
jobsJSONstrBadKey2 = r"""
{"job1":
	{
	"filepath": "c:\\Program Files (x86)\\Steam\\steamapps\\common\\rFactor 2\\UserData\\player\\player.json",

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
	"filepath": "c:\\Program Files (x86)\\Steam\\steamapps\\common\\rFactor 2\\UserData\\player\\player.json",

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
"""
valid_JSON_strings.append(jobsJSONstrBadKey2)

# Valid JSON but key name is wrong
jobsJSONstrBadKey = r"""
{"job1":
	{
	"filepath": "c:\\Program Files (x86)\\Steam\\steamapps\\common\\rFactor 2\\UserData\\player\\player.json",

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
"""
valid_JSON_strings.append(jobsJSONstrBadKey)

jobsBadJSONstr = r"""
{"job1":
	{
	"filepath": "c:\\Program Files (x86)\\Steam\\steamapps\\common\\rFactor 2\\UserData\\player\\player.json",

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
        assert True, 'JSON string content error'

  def test_invalid_JSON_strings(self):
    for json_str in invalid_JSON_strings:
      try:
        json_dict = json.loads(json_str)
        assert True, 'JSON string content error expected but didn\'t happen'
      except ValueError:
        pass # Error is expected

if __name__ == '__main__':
  unittest.main()
