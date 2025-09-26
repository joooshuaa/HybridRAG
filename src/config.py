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
LIGHTRAG_LLM_NAME = 'qwen3:30b-a3b-instruct-2507-q8_0' #'gemma3:4b-it-qat' #'qwen3:0.6b' #'gemma3:12b-it-q4_K_M'
#LIGHTRAG_BASE_URL = "http://localhost:9621"
LIGHTRAG_LLM_MAX_TOKEN_SIZE = 65536 #131072 # 32768
LIGHTRAG_MAX_PARALLEL_INSERT = 2
LIGHTRAG_EMBEDDING_MODEL_NAME = 'bge-m3:latest' #"nomic-embed-text:latest"
LIGHTRAG_EMBEDDING_MAX_TOKEN_SIZE = 6144
LIGHTRAG_EMBEDDING_DIM = 1024

# OLLAMA