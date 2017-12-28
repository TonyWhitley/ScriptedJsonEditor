import os
import sys
import unittest

import ScriptedJsonEditor

#sys.path.insert(0, 
this_folder = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

def this_path(filename):
  return os.path.join(this_folder, filename)

JSONstr1 = r"""
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

class Test_test_jobs(unittest.TestCase):
    def test_read_0(self):
        filepath = this_path('no_such_file.json')
        _jsonO = ScriptedJsonEditor.JsonFile()
        pJson = _jsonO.read(filepath)
        assert pJson == None
    def test_read_file(self):
        filepath = this_path('jobs_test1.json')
        _jsonO = ScriptedJsonEditor.JsonFile()
        pJson = _jsonO.read(filepath)
        assert pJson["job1"] != None
        assert pJson["job1"]["filepath"] != None
        assert len(pJson["job1"]["edits"]) > 0, pJson["job1"]["edits"]
    def test_load_JSON_str(self):
        _jsonO = ScriptedJsonEditor.JsonFile()
        pJson = _jsonO._load(JSONstr1)
        assert pJson["job1"] != None
        assert pJson["job1"]["filepath"] != None
        assert len(pJson["job1"]["edits"]) > 0, pJson["job1"]["edits"]
    def test_get_jobs(self):
        _jsonO = ScriptedJsonEditor.JsonFile()
        pJson = _jsonO._load(JSONstr1)
        assert pJson["job1"] != None
        assert pJson["job1"]["filepath"] != None
        assert len(pJson["job1"]["edits"]) > 0, pJson["job1"]["edits"]
        jobs = _jsonO.getJobs()
        assert len(jobs) > 0
        assert jobs[0]["filepath"] != None
        assert len(jobs[0]["edits"]) > 0, jobs[0]["edits"]



if __name__ == '__main__':
    unittest.main()
  