import re
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_all_tools(lines):
    """Extract all tool numbers from NC file lines."""
    logger.debug("Extracting tool numbers from lines")
    tools = set()
    for line in lines:
        if line.lstrip().startswith('/'):
            continue
        matches = re.findall(r'(?<!\w)T(\d+)(?!\d)', line)
        tools.update(int(m) for m in matches)
    logger.debug(f"Extracted {len(tools)} unique tool numbers")
    return tools

def safe_remap_nc_file(input_path, output_path, remap_map):
    """Remap tool numbers in an NC file and save the output."""
    logger.debug(f"Remapping file: {input_path} to {output_path}")
    try:
        with open(input_path, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        logger.error(f"Failed to read input file {input_path}: {str(e)}")
        return {"success": False, "error": f"Failed to read input file: {str(e)}"}

    remap_map = {int(k): int(v['new_t']) for k, v in remap_map.items()}
    logger.debug(f"Remap map: {remap_map}")

    existing_tools = extract_all_tools(lines)
    new_t_set = set(remap_map.values())

    # Check for duplicates
    for new_t in new_t_set:
        if new_t in existing_tools and new_t not in remap_map.keys():
            error_msg = f"Duplicate tool number detected: T{new_t}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}

    new_lines = []
    current_tool = None

    for line in lines:
        # Preserve the original line, including its ending
        original_line = line
        stripped_line = original_line.rstrip('\r\n')
        logger.debug(f"Processing line: {stripped_line}")

        # Initialize newline as the stripped line
        newline = stripped_line

        # Handle block skip lines
        if stripped_line.lstrip().startswith('/'):
            new_lines.append(original_line)
            continue

        # Handle empty lines or lines with only whitespace
        if not stripped_line:
            new_lines.append(original_line)
            continue

        # Handle header lines
        header_match = re.match(r'\(T(\d+)\|.*?\|H(\d+)\|D(\d+)\|', newline)
        if header_match:
            old_t = int(header_match.group(2))
            if old_t in remap_map:
                new_t = remap_map[old_t]
                newline = re.sub(r'T\d+', f"T{new_t}", newline, 1)
                newline = re.sub(r'H\d+', f"H{new_t}", newline)
                newline = re.sub(r'D\d+', f"D{new_t}", newline)
                logger.debug(f"Remapped header: {newline}")
            new_lines.append(newline)
            continue

        # Handle tool changes and offsets
        t_match = re.search(r'(?<!\w)T(\d+)(?!\d)', newline.upper())
        if t_match:
            t_val = int(t_match.group(1))
            if 'M6' in newline.upper():
                current_tool = t_val
                logger.debug(f"Set current tool: T{current_tool}")
            if t_val in remap_map:
                new_t = remap_map[t_val]
                newline = re.sub(rf'(?<!\w)T{t_val}(?!\d)', f"T{new_t}", newline)
                logger.debug(f"Remapped tool: T{t_val} to T{new_t}")

        if current_tool in remap_map and 'H' in newline.upper():
            old_h = remap_map[current_tool]
            newline = re.sub(r'H\d+', f"H{old_h}", newline)
            logger.debug(f"Remapped height offset: H{old_h}")

        if current_tool in remap_map and 'D' in newline.upper():
            old_d = remap_map[current_tool]
            newline = re.sub(r'D\d+', f"D{old_d}", newline)
            logger.debug(f"Remapped diameter offset: D{old_d}")

        new_lines.append(newline)


    try:
        with open(output_path, 'w') as f:
            f.writelines(new_lines)
        logger.info(f"Successfully wrote remapped file to {output_path}")
        return {"success": True}
    except Exception as e:
        logger.error(f"Failed to write output file {output_path}: {str(e)}")
        return {"success": False, "error": f"Failed to write output file: {str(e)}"}