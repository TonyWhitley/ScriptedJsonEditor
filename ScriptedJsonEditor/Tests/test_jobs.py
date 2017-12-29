import os
import sys
import unittest

import ScriptedJsonEditor

#sys.path.insert(0, 
this_folder = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

def this_path(filename):
  return os.path.join(this_folder, filename)

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

jobsJSONstr2 = r"""
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

class Test_test_jobs(unittest.TestCase):
    def test_read_0(self):
        filepath = this_path('no_such_file.json')
        _JSNO_O = ScriptedJsonEditor.JsonFile()
        P_JSON = _JSNO_O.read(filepath)
        assert P_JSON == None
    def test_read_file(self):
        filepath = this_path('jobs_test1.json')
        _JSNO_O = ScriptedJsonEditor.JsonFile()
        P_JSON = _JSNO_O.read(filepath)
        assert P_JSON["job1"] != None
        assert P_JSON["job1"]["filepath"] != None
        assert len(P_JSON["job1"]["edits"]) > 0, P_JSON["job1"]["edits"]
    def test_load_JSON_str(self):
        _JSNO_O = ScriptedJsonEditor.JsonFile()
        P_JSON = _JSNO_O._load(jobsJSONstr1)
        assert P_JSON["job1"] != None
        assert P_JSON["job1"]["filepath"] != None
        assert len(P_JSON["job1"]["edits"]) > 0, P_JSON["job1"]["edits"]
    def test_get_jobs(self):
        _JSNO_O = ScriptedJsonEditor.JsonFile()
        P_JSON = _JSNO_O._load(jobsJSONstr1)
        assert P_JSON["job1"] != None
        assert P_JSON["job1"]["filepath"] != None
        assert len(P_JSON["job1"]["edits"]) > 0, P_JSON["job1"]["edits"]
        jobs = _JSNO_O.get_jobs()
        assert len(jobs) > 0
        assert jobs[0]["filepath"] != None
        assert len(jobs[0]["edits"]) > 0, jobs[0]["edits"]

    def test_load_JSON_str_2jobs(self):
        _JSNO_O = ScriptedJsonEditor.JsonFile()
        P_JSON = _JSNO_O._load(jobsJSONstr2)
        assert P_JSON["job1"] != None
        assert P_JSON["job1"]["filepath"] != None
        assert len(P_JSON["job1"]["edits"]) > 0, P_JSON["job1"]["edits"]
        assert P_JSON["job2"] != None
        assert P_JSON["job2"]["filepath"] != None
        assert len(P_JSON["job2"]["edits"]) > 0, P_JSON["job2"]["edits"]
    def test_get_2jobs(self):
        _JSNO_O = ScriptedJsonEditor.JsonFile()
        P_JSON = _JSNO_O._load(jobsJSONstr2)
        assert P_JSON["job1"] != None
        assert P_JSON["job1"]["filepath"] != None
        assert len(P_JSON["job1"]["edits"]) > 0, P_JSON["job1"]["edits"]
        assert P_JSON["job2"] != None
        assert P_JSON["job2"]["filepath"] != None
        assert len(P_JSON["job2"]["edits"]) > 0, P_JSON["job2"]["edits"]
        jobs = _JSNO_O.get_jobs()
        assert len(jobs) > 0
        assert jobs[0]["filepath"] != None
        assert len(jobs[0]["edits"]) > 0, jobs[0]["edits"]
        assert jobs[1]["filepath"] != None
        assert len(jobs[1]["edits"]) > 0, jobs[1]["edits"]


if __name__ == '__main__':
    unittest.main()
  