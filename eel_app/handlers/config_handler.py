import eel
import os
import json

@eel.expose
def load_config():
    """Load configuration from config.json."""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "save_location": "",
            "data_location": "",
            "remap_suffix": "_remapped",
            "toolchange_codes": "M6,M06,M106",
            "height_offset_codes": "G43,G243",
            "diameter_comp_codes": "G41,G42",
            "cancel_comp_code": "G40",
            "search_terms": ["", "", "", "", ""],
            "search_enabled": [True, True, True, True, True],
            "features": {
                "comments": False,
                "thd": False,
                "thd_h_match": False,
                "thd_d_match": False,
                "speeds": False,
                "speeds_tap_m5": False
            }
        }
    except Exception as e:
        return {"error": f"Failed to load config: {str(e)}"}

@eel.expose
def save_config(config):
    """Save configuration to config.json."""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": f"Failed to save config: {str(e)}"}