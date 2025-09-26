import asyncio
import logging
import os
import json

from lightrag import LightRAG
from lightrag.llm.ollama import ollama_model_complete, ollama_embed
from lightrag.kg.shared_storage import initialize_pipeline_status
from lightrag.utils import EmbeddingFunc, setup_logger, TokenTracker

from config import *

from .base import BaseRetriever

logger = logging.getLogger(__name__)


class KGLightRAG(BaseRetriever):

    __rag = None
    __token_tracker = None

    def __init__(self):
        if not os.path.exists(LIGHTRAG_STORAGE_DIR):
            os.mkdir(LIGHTRAG_STORAGE_DIR)

        self.__rag = LightRAG(
            working_dir=LIGHTRAG_STORAGE_DIR,
            llm_model_func=ollama_model_complete,  # Use Ollama model for text generation
            llm_model_name=LIGHTRAG_LLM_NAME,
            llm_model_kwargs={"options": {"num_ctx": LIGHTRAG_LLM_MAX_TOKEN_SIZE}},
            max_parallel_insert=LIGHTRAG_MAX_PARALLEL_INSERT,
            # Use Ollama embedding function
            embedding_func=EmbeddingFunc(
                embedding_dim=LIGHTRAG_EMBEDDING_DIM,
                max_token_size=LIGHTRAG_LLM_MAX_TOKEN_SIZE,
                # seems to have no effect when func=ollama_embed, bc ollama_embed does not use this arg/kwarg
                func=lambda texts: ollama_embed(
                    texts,
                    embed_model=LIGHTRAG_EMBEDDING_MODEL_NAME
                )
            ),
        )
        # IMPORTANT: Both initialization calls are required!
        asyncio.run(self.__rag.initialize_storages())  # Initialize storage backends
        asyncio.run(initialize_pipeline_status())  # Initialize processing pipeline

        self.__token_tracker = TokenTracker()

    def index(self, directory: str) -> None:
        raise NotImplementedError()

    async def aindex(self, directory: str) -> None:
        setup_logger("lightrag", level="DEBUG")

        try:
            document_files = os.listdir(directory)
            ids, documents, file_paths = [], [], []
            document = ""
            iteration = 1
            chunk_separator = "\n"

            async def ins(d, i, p):
                with self.__token_tracker:
                    await self.__rag.ainsert(d, split_by_character=chunk_separator, split_by_character_only=False,
                                             ids=i, file_paths=p)

            async def create_manual_docs_from_lines():
                for document_file in document_files:
                    full_file_path = os.path.join(DATA_DIR_PATH, document_file)
                    print("opening file " + full_file_path)
                    with open(full_file_path, 'r') as f:
                        for line in f:
                            line = json.loads(line)
                            document += line["title"] + ": " + line["text"] + ";"
                            if len(document) > (LIGHTRAG_LLM_MAX_TOKEN_SIZE - 10000):
                                ids.append(document_file + "_iter_" + str(iteration))
                                file_paths.append(document_file)
                                documents.append(document)
                                document = ""
                                iteration += 1
                            if iteration % 12 == 0:
                                print("iteration " + str(iteration))
                                with token_tracker:
                                    await ins(documents, ids, file_paths)
                                print("Token usage after iteration ", iteration, ": ", str(token_tracker.get_usage()))
                                documents = []
                                ids = []
                                file_paths = []
                print(str(ids))
                if len(document) > 0:
                    ids.append(document_file + "_iter_" + str(iteration))
                    file_paths.append(document_file)
                    documents.append(document)
                if iteration % 12 != 0:
                    await ins(documents, ids, file_paths)

            async def document_per_line():
                for document_file in document_files:
                    full_file_path = os.path.join(DATA_DIR_PATH, document_file)
                    print("opening file " + full_file_path)
                    with open(full_file_path, 'r') as f:
                        for line in f:
                            line = json.loads(line)
                            ids.append(document_file + "_iter_" + str(iteration) + "_id_" + str(line["_id"]))
                            file_paths.append(document_file)
                            document = line["title"] + ": " + line["text"] + ";"
                            documents.append(document)
                            iteration += 1
                            if iteration % 12 == 0:
                                with token_tracker:
                                    await ins(documents, ids, file_paths)
                                print("Token usage after iteration ", iteration, ": ", str(token_tracker.get_usage()))
                                documents = []
                                ids = []
                                file_paths = []
                if iteration % 12 != 0:
                    await ins(documents, ids, file_paths)

            for document_file in document_files:
                full_file_path = os.path.join(DATA_DIR_PATH, document_file)
                with open(full_file_path, 'r') as f:
                    document = ""
                    for line in f:
                        line = json.loads(line)
                        document += line["title"] + ": " + line["text"] + "\n"
                ids.append(document_file + "_iter_" + str(iteration))
                file_paths.append(document_file)
                documents.append(document)
                iteration += 1
                if iteration % 1 == 0:
                    await ins(documents, ids, file_paths)
                    print("Token usage after iteration ", iteration, ": ", str(self.__token_tracker.get_usage()))
                    ids, documents, file_paths = [], [], []
            if iteration % 12 != 0:
                await ins(documents, ids, file_paths)

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if self.__rag:
                print("total token usage: ", str(self.__token_tracker.get_usage()))
                await self.__rag.finalize_storages()

    def retrieve(self, file_content: bytes, filename: str, content_type: str = None) -> str:
        pass

    @property
    def retriever_name(self) -> str:
        return "Knowledge Graph Light RAG"