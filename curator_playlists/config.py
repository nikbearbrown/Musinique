import os 
from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
MAX_RETRIES = 7    
CURATOR_START_INDEX = 96
CURATOR_END_INDEX = 100