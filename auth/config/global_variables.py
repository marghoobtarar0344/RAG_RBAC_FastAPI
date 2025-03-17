import os
from dotenv import load_dotenv
load_dotenv()

# *************** swagger **************#
TITLE = "RBAC-RAG PIPELINE"
VERSION = "V-0.0.0"
DESCRIPTION = "This is RBAC RAG Pipeline description which appears on the swagger"

# *************** FAST API *************
CROS_ORIGIN = ['*']
ALLOWED_METHODS = ['*']
ALLOWED_HEADERS = ['*']
ALLOWED_CREDENTIALS = True

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DATABASE_URL = os.getenv("DATABASE_URL")

