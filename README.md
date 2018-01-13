# ScriptedJsonEditor
Scripted JSON editor is a command line program to make changes for example to rFactor 2 player.json

Rather than a list of instructions to "edit player.json setting 'blah' to 15" and so on, instead provide a JSON file (or just the text to paste into one) then run ScriptedJsonEditor.

To run it, open a cmd window and enter (as an example)

 ScriptedJsonEditor jobs/keyboard.json

An example jobs file is

	{
	  "<CONTROLLER.JSON>": "c:\\Program Files (x86)\\Steam\\steamapps\\common\\rFactor 2\\UserData\\Player\\Controller.JSON",
	  "jobs file format": 6,
	  "job definition files": [
	    "job definitions\\Keyboard_jobs.json"
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


That makes use of the one of the "Jobs definition files" Keyboard_jobs.json
that handles the details of the edits.  These files are shared (though you
are of course free to edit them).
Example contents of that are:

	{
	  "# Keyboard - job definitions file for ScriptedJsonEditor": "",
	  "# V1.0.0": "",
	  "# Note: any key with a # is a comment": "",
	  "job definitions": {
	    "Cursor keys control seat": {
	      "JSONfileToBeEdited": "<CONTROLLER.JSON>",
	      "edits": {
		"Input": {
		  "# Cursor keys control seat": 0,
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

For a full example see jobs\VR_G25.json.

Here is a Mind Map that shows the contents of the job and job definition files:

![data file
2](https://raw.githubusercontent.com/TonyWhitley/ScriptedJsonEditor/master/DataFiles.jpeg)

