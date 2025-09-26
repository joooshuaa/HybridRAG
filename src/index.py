from config import *
from retrievers import HybridRetriever


if __name__ == "__main__":
    retriever = HybridRetriever()
    retriever.index(DATA_DIR_PATH)
