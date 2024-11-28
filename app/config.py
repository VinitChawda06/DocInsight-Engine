import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Directory paths
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
VECTOR_DIR = DATA_DIR / "vectors"
# Add these to your config.py
CACHE_DIR = DATA_DIR / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Model settings
N_GPU_LAYERS = int(os.getenv("N_GPU_LAYERS", "1"))
MODEL_CACHE_DIR = str(CACHE_DIR / "models")

# Model settings
MODEL_PATH = os.getenv("MODEL_PATH", "models/mistral-7b-instruct-v0.2.Q4_K_M.gguf")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", str(VECTOR_DIR))

# App settings
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))

# Document processing settings
MAX_CHUNK_SIZE = int(os.getenv("MAX_CHUNK_SIZE", "512"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))

# Create directories if they don't exist
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, VECTOR_DIR]:
    directory.mkdir(parents=True, exist_ok=True)