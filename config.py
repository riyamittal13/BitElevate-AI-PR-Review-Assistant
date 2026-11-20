# import os

# from dotenv import load_dotenv

# load_dotenv()

# GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# GITHUB_API_URL = "https://api.github.com"
# REQUEST_TIMEOUT = 20
# MAX_FILES = 30


import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_secret(name):
    value = os.getenv(name, "")
    if value:
        return value

    try:
        return st.secrets.get(name, "")
    except (FileNotFoundError, RuntimeError):
        return ""

GITHUB_TOKEN = get_secret("GITHUB_TOKEN")
GEMINI_API_KEY = get_secret("GEMINI_API_KEY")

GITHUB_API_URL = "https://api.github.com"
REQUEST_TIMEOUT = 20
MAX_FILES = 30