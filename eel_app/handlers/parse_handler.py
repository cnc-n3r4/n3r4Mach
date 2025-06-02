import eel
import os
import json
from backend.parser_coordinator import parse_gcode_file

@eel.expose
def parse_gcode_file(filename):
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {
            "save_location": os.path.join(os.path.dirname(__file__), '..', 'output'),
            "data_location": os.path.join(os.path.dirname(__file__), '..', 'data'),
            "api_key": "",
            "toolchange_codes": "M6,M06,M106",
            "height_offset_codes": "G43,G243",
            "diameter_comp_codes": "G41,G42",
            "cancel_comp_code": "G40",
            "features": {
                "comments": True,
                "thd": True,
                "thd_h_match": True,
                "thd_d_match": True,
                "speeds": True,
                "speeds_tap_m5": False
            }
        }
    
    settings = {
        "toolchange_codes": [code.strip() for code in config["toolchange_codes"].split(",")],
        "height_offset_codes": [code.strip() for code in config["height_offset_codes"].split(",")],
        "diameter_comp_codes": [code.strip() for code in config["diameter_comp_codes"].split(",")],
        "cancel_comp_code": config["cancel_comp_code"],
        "features": config["features"],
        "api_key": config["api_key"],
        "data_folder": config["data_location"]
    }
    
    input_path = os.path.join(os.path.dirname(__file__), '..', 'temp', filename)
    return parse_gcode_file(input_path, settings)