# ScriptedJsonEditor
Scripted JSON editor to make changes for example to rFactor 2 player.json

Rather than a list of instructions to "edit player.json setting 'blah' to 15" and so on, instead provide a JSON file (or just the text to paste into one) then run ScriptedJsonEditor.

An example file is

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
