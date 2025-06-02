import eel
import os
import json
import logging
from backend.tool_parser import parse_nc_tools
from backend.remapper import safe_remap_nc_file

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@eel.expose
def analyze_nc_file(path):
    """Parse an NC file to extract tool numbers and offsets."""
    logger.debug(f"analyze_nc_file called with path: {path}")
    try:
        input_path = os.path.join(os.path.dirname(__file__), '..', path)
        logger.debug(f"Resolved input path: {input_path}")
        if not os.path.isfile(input_path):
            logger.error(f"File not found: {input_path}")
            return {"error": f"File not found: {input_path}"}
        tools = parse_nc_tools(input_path)
        if not tools:
            logger.warning("No valid tools found in the file")
            return {"error": "No valid tools found in the file"}
        logger.debug(f"Parsed {len(tools)} tools")
        return tools
    except Exception as e:
        logger.error(f"Failed to parse file: {str(e)}")
        return {"error": f"Failed to parse file: {str(e)}"}

@eel.expose
def remap_and_save(remap_map, input_file, output_file):
    """Remap tool numbers in an NC file and save the output."""
    logger.debug(f"remap_and_save called with input_file: {input_file}, output_file: {output_file}")
    try:
        # Load config to get Save Location and suffix
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
        logger.debug(f"Loading config from: {config_path}")
        if not os.path.isfile(config_path):
            logger.error("Configuration file not found: config.json")
            return {"error": "Configuration file not found: config.json"}
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        save_location = config.get("save_location", "")
        data_location = config.get("data_location", "")
        if not save_location or not os.path.isdir(save_location):
            logger.error(f"Invalid or missing Save Location in config: {save_location}")
            return {"error": f"Invalid or missing Save Location in config: {save_location}"}
        if not data_location or not os.path.isdir(data_location):
            logger.error(f"Invalid or missing Data Location in config: {data_location}")
            return {"error": f"Invalid or missing Data Location in config: {data_location}"}
        
        # Validate unique new tool numbers
        new_tools = [v['new_t'] for v in remap_map.values()]
        if len(new_tools) != len(set(new_tools)):
            error_msg = "Duplicate new tool numbers detected in remap map"
            logger.error(error_msg)
            # Log to file in Data Location
            log_file = os.path.join(data_location, 'error.log')
            os.makedirs(data_location, exist_ok=True)
            with open(log_file, 'a') as f:
                f.write(f"{logging.getLogger().handlers[0].formatter.format(logging.makeLogRecord({'asctime': logging.Formatter().formatTime(logging.makeLogRecord({})), 'levelname': 'ERROR', 'message': error_msg}))}\n")
            return {"error": error_msg}
        
        # Construct full input/output paths
        input_path = os.path.join(os.path.dirname(__file__), '..', input_file)
        logger.debug(f"Resolved input path: {input_path}")
        if not os.path.isfile(input_path):
            logger.error(f"Input file not found: {input_path}")
            return {"error": f"Input file not found: {input_path}"}
        
        output_filename = os.path.basename(input_file).replace(
            os.path.splitext(input_file)[1],
            config.get("remap_suffix", "_remapped") + os.path.splitext(input_file)[1]
        )
        output_path = os.path.join(save_location, output_filename)
        logger.debug(f"Resolved output path: {output_path}")
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Perform remapping
        logger.debug(f"Remapping with map: {remap_map}")
        result = safe_remap_nc_file(input_path, output_path, remap_map)
        if not result["success"]:
            logger.error(f"Remapping failed: {result.get('error', 'Unknown error')}")
            # Log to file in Data Location
            log_file = os.path.join(data_location, 'error.log')
            with open(log_file, 'a') as f:
                f.write(f"{logging.getLogger().handlers[0].formatter.format(logging.makeLogRecord({'asctime': logging.Formatter().formatTime(logging.makeLogRecord({})), 'levelname': 'ERROR', 'message': result.get('error', 'Unknown remapping error')}))}\n")
            return {"error": result.get("error", "Unknown remapping error")}
        
        logger.info(f"Remapped file saved to {output_path}")
        return {"success": True, "message": f"Remapped file saved to {output_path}"}
    except Exception as e:
        logger.error(f"Failed to remap and save: {str(e)}")
        # Log to file in Data Location
        log_file = os.path.join(data_location, 'error.log')
        os.makedirs(data_location, exist_ok=True)
        with open(log_file, 'a') as f:
            f.write(f"{logging.getLogger().handlers[0].formatter.format(logging.makeLogRecord({'asctime': logging.Formatter().formatTime(logging.makeLogRecord({})), 'levelname': 'ERROR', 'message': str(e)}))}\n")
        return {"error": f"Failed to remap and save: {str(e)}"}