""" Utility file to write Python data structure as JSON string. """
import json
import pprint

_DATA = {
    "<CONTROLLER.JSON>":
    r"c:\Program Files (x86)\Steam\steamapps\common\rFactor 2\UserData\Player\Controller.JSON",
    "job definition files": ["Keyboard_jobs.json"],
    "jobs": [
        {"Keyboard_jobs": [
            "Driver aid buttons disable",
            "Cursor keys control seat"]
         }
    ]
}

PP = pprint.PrettyPrinter(indent=2)
PP.pprint(_DATA)
print()
_JSON_STR = json.dumps(_DATA, indent=2)
print(_JSON_STR)

json.loads(_JSON_STR)
