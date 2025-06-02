import eel
import logging
import os
from handlers import file_handler, config_handler, remap_handler, calc_handler

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

eel.init('web')

chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
 
eel.start(
    "index.html",
    mode=chrome_path,
    size=(800, 600),
    port=8000
)

# Log all page requests
@eel.expose
def log_page_request(page):
    logger.debug(f"Request for page: {page}")
    if not os.path.isfile(os.path.join('web', page)):
        logger.error(f"Page not found: web/{page}")
    return {"status": "received"}

if __name__ == '__main__':
    try:
        logger.info("Starting Eel application on http://localhost:8000")
        # Verify web directory
        web_dir = os.path.join(os.path.dirname(__file__), 'web')
        if not os.path.isdir(web_dir):
            logger.error(f"Web directory not found: {web_dir}")
            raise FileNotFoundError(f"Web directory not found: {web_dir}")
        
        # Check for key HTML files
        for page in ['index.html', 'config.html', 'calculator.html', 'remap.html']:
            if not os.path.isfile(os.path.join(web_dir, page)):
                logger.warning(f"HTML file missing: web/{page}")
        
    except Exception as e:
        logger.error(f"Failed to start Eel application: {str(e)}")
        raise