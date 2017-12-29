import unittest
import ScriptedJsonEditor

filepath = r'c:\Program Files (x86)\Steam\steamapps\common\rFactor 2\UserData\player\player.json'

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
                            "Car Vibration Mult2#":"Secondary engine vibration multiplier affects orientation of cameras attached directly to the car"
  }
}
"""

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

class Test_test_JSON(unittest.TestCase):
    def test_readJsonFile(self):
        _JSNO_O = ScriptedJsonEditor.JsonFile()
        P_JSON = _JSNO_O.read(filepath)
        _filepath = filepath + '.mostlySame'
        _JSNO_O.write(_filepath)

    def test_editJson(self):
        _JSNO_O = ScriptedJsonEditor.JsonFile()
        P_JSON = _JSNO_O.read(filepath)
        ##################################
        # change values as required
        ##################################
        for key, item, newValue in edits:
          _JSNO_O.edit(key, item, newValue)
  
        _filepath = filepath + '.edited'
        _JSNO_O.write(_filepath)

    def test_get_jobs(self):
        _jsonJob = ScriptedJsonEditor.JsonFile()
        P_JSON = _jsonJob._load(jobsJSONstr)
        assert P_JSON["job1"] != None
        assert P_JSON["job1"]["filepath"] != None
        assert len(P_JSON["job1"]["edits"]) > 0, P_JSON["job1"]["edits"]
        jobs = _jsonJob.get_jobs()
        assert len(jobs) > 0
        assert jobs[0]["filepath"] != None
        assert len(jobs[0]["edits"]) > 0, jobs[0]["edits"]
        
        _JSNO_O = ScriptedJsonEditor.JsonFile()
        P_JSON = _JSNO_O._load(playerJSONstr)
        assert P_JSON["Graphic Options"] != None
        assert P_JSON["Graphic Options"]["Allow HUD in cockpit"] != None
        assert P_JSON["Graphic Options"]["Allow HUD in cockpit"], P_JSON["Graphic Options"]["Allow HUD in cockpit"]

        # This is only what run_jobs() does 
        for job in jobs:
          for main_key in job["edits"]:
            for item in job["edits"][main_key]:
              _JSNO_O.edit(main_key, item, job["edits"][main_key][item])

        assert _JSNO_O._get_value("Graphic Options", "Allow Letterboxing") == False, _JSNO_O._get_value("Graphic Options", "Allow Letterboxing")

    def test_run_jobs(self):
        _jsonJob = ScriptedJsonEditor.JsonFile()
        P_JSON = _jsonJob._load(jobsJSONstr)
        assert P_JSON["job1"] != None
        assert P_JSON["job1"]["filepath"] != None
        assert len(P_JSON["job1"]["edits"]) > 0, P_JSON["job1"]["edits"]
        jobs = _jsonJob.get_jobs()
        assert len(jobs) > 0
        assert jobs[0]["filepath"] != None
        assert len(jobs[0]["edits"]) > 0, jobs[0]["edits"]
        
        _JSNO_O = ScriptedJsonEditor.JsonFile()
        P_JSON = _JSNO_O._load(playerJSONstr)
        assert P_JSON["Graphic Options"] != None
        assert P_JSON["Graphic Options"]["Allow HUD in cockpit"] != None
        assert P_JSON["Graphic Options"]["Allow HUD in cockpit"], P_JSON["Graphic Options"]["Allow HUD in cockpit"]

        _JSNO_O.run_jobs(jobs)

        assert _JSNO_O._get_value("Graphic Options", "Allow Letterboxing") == False, _JSNO_O._get_value("Graphic Options", "Allow Letterboxing")
        
if __name__ == '__main__':
    unittest.main()
