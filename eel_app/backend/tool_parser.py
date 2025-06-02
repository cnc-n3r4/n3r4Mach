import re
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_nc_tools(path):
    """Parse an NC file to extract tool numbers (T), height offsets (H), and diameter offsets (D)."""
    logger.debug(f"Parsing NC file: {path}")
    try:
        with open(path, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        logger.error(f"Failed to open file {path}: {str(e)}")
        return []

    tools = []
    seen = set()
    current_tool = None
    d_counts = {}  # Track D values and their counts for each tool

    for i, line in enumerate(lines):
        line = line.strip()
        if not line or line.startswith('(') or line.startswith('%'):
            continue

        upper_line = line.upper()

        # Detect tool changes (T with M6)
        if 'T' in upper_line and 'M6' in upper_line:
            t_match = re.search(r'T(\d+)', upper_line)
            if t_match:
                current_tool = int(t_match.group(1))
                logger.debug(f"Found tool change: T{current_tool} at line {i+1}")
                d_counts[current_tool] = {}  # Initialize D counts for this tool
                continue

        # Detect height offsets (G43 with H) and diameter offsets (D in same line)
        if current_tool is not None and 'G43' in upper_line and 'H' in upper_line:
            h_match = re.search(r'H(\d+)', upper_line)
            h_val = int(h_match.group(1)) if h_match else current_tool
            logger.debug(f"Found height offset: H{h_val} for T{current_tool} at line {i+1}")

            d_vals = []
            for d_match in re.finditer(r'D(\d+)', upper_line):
                d_val = int(d_match.group(1))
                d_counts[current_tool][d_val] = d_counts[current_tool].get(d_val, 0) + 1
                if d_val not in d_vals:
                    d_vals.append(d_val)
                logger.debug(f"Found diameter offset: D{d_val} for T{current_tool} at line {i+1}")

            if current_tool not in seen:
                tools.append({
                    't': current_tool,
                    'h': h_val,
                    'd': [{'value': d, 'count': d_counts[current_tool][d]} for d in d_vals]
                })
                seen.add(current_tool)

        # Detect diameter offsets in G41/G42 (cutter compensation) or standalone D commands
        if current_tool is not None and ('G41' in upper_line or 'G42' in upper_line or re.search(r'\bD\d+\b', upper_line)):
            for d_match in re.finditer(r'D(\d+)', upper_line):
                d_val = int(d_match.group(1))
                d_counts[current_tool][d_val] = d_counts[current_tool].get(d_val, 0) + 1
                logger.debug(f"Found diameter offset: D{d_val} for T{current_tool} at line {i+1}")

                # Update existing tool entry if already seen
                for tool in tools:
                    if tool['t'] == current_tool:
                        if not any(d['value'] == d_val for d in tool['d']):
                            tool['d'].append({'value': d_val, 'count': d_counts[current_tool][d_val]})
                        else:
                            for d in tool['d']:
                                if d['value'] == d_val:
                                    d['count'] = d_counts[current_tool][d_val]
                        break

    logger.debug(f"Parsed {len(tools)} tools from {path}")
    return tools