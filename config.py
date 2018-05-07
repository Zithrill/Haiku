import os
import logging
import re

class Config:

    # FETCHING DATA
    HAIKU_BASE_URL = 'http://www.tempslibres.org/tl/tlphp/'
    HAIKU_URL = HAIKU_BASE_URL + 'dbauteurs.php?lg=e'

    HAIKU_PARTIAL_HREF_REGEX = re.compile('dbhk01\.php\?auteur.*\&lg=e')

    SOUP_PARSER = 'html5lib'

    FETCH_DELAY_IN_SEC = 1 # Not needed we just want to be nice

    # SYSTEM DIRECTORIES
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    
    RESOURCE_PATH = os.path.join(ROOT_DIR, 'resources')
    HAIKU_PATH =  os.path.join(RESOURCE_PATH, 'haiku')
    RAW_HAIKU_PATH =  os.path.join(HAIKU_PATH, 'html')
    PROCESSED_HAIKU_PATH = os.path.join(HAIKU_PATH, 'json')
    HAIKU_JSON_NAME = 'haiku.json'
    HAIKU_JSON_LOCATION =  os.path.join(PROCESSED_HAIKU_PATH, HAIKU_JSON_NAME)

    # LOG
    LOG_LEVEL = logging.DEBUG # See https://docs.python.org/3/library/logging.html#logging-levels
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL) 
