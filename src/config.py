# Retrievers
from pathlib import Path
import os

WORKDIR = os.getcwd() + '/workdir/hotpotqa'
DATA_DIR_PATH = WORKDIR + '/docs'


# FAISS
FAISS_STORAGE_DIR = WORKDIR + "/faiss_index_store"
FAISS_INDEX_FILENAME = "faiss.index"
FAISS_EMBED_MODEL_NAME = "intfloat/multilingual-e5-base"
FAISS_EMBEDDING_DIM = 768 #384

# LIGHTRAG
LIGHTRAG_STORAGE_DIR = WORKDIR + "/rag_storage"
LIGHTRAG_LLM_NAME = 'gemma3:4b-it-qat' #'qwen3:0.6b' #'gemma3:12b-it-q4_K_M'
#LIGHTRAG_BASE_URL = "http://localhost:9621"
LIGHTRAG_LLM_MAX_TOKEN_SIZE = 32768
LIGHTRAG_MAX_PARALLEL_INSERT = 3
LIGHTRAG_EMBEDDING_MODEL_NAME = "nomic-embed-text:latest"
LIGHTRAG_EMBEDDING_DIM = 768

# OLLAMA