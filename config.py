import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Application configuration
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
PORT = os.getenv('PORT')
JENKINS_URL = os.getenv('JENKINS_URL')
JENKINS_CRED = json.loads(os.getenv('JENKINS_CRED'))