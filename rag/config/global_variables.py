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
VECTOR_DB_PATH = "chroma_db"
HUGGING_FACE_MODEL="sentence-transformers/all-MiniLM-L12-v2"
RECURSIVE_SPLITTER_CHUNK_SIZE=500
RECURSIVE_SPLITTER_CHUNK_OVERLAP=50

