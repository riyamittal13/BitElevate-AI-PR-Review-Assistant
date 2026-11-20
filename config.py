import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

GITHUB_API_URL = "https://api.github.com"
REQUEST_TIMEOUT = 20
MAX_FILES = 30