# ScriptedJsonEditor
Scripted JSON editor to make changes for example to rFactor 2 player.json

Rather than a list of instructions to "edit player.json setting 'blah' to 15" and so on, instead provide a JSON file (or just the text to paste into one) then run ScriptedJsonEditor.

An example file is

    {"job1":
      {
      "JSONfileToBeEdited": "c:\\Program Files (x86)\\Steam\\steamapps\\common\\rFactor 2\\UserData\\player\\player.json",
      "skip keys with # in them": true,
      "# keys with # in them are used as comments, don't change the values": 0,
      "rFactor escape slash": true,
      "# rFactor 2 escapes /. Also remove space after the :": 0,

      "edits": {
        "Graphic Options":{
            "Allow Letterboxing":false,
            "Allow Letterboxing#":"whether we allow letterboxing (during replays, for example)",
            "Automap":3,
            "Automap#":"0=off 1=race-only 2=non-race-only 3=all sessions"
          }
        }
      }
    }
