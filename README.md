## Prerequisites

Ollama needs to be installed on the machine

```console
curl -fsSL https://ollama.com/install.sh | sh
```

The to be used models have to be pulled with ollama.
Model names are configured in /src/config.py

```console
ollama pull qwen3:30b-a3b-instruct-2507-q8_0
ollama pull bge-m3:latest
```

## Start indexing pipeline

Start in the project root directory and execute the pipeline from there

```console
user@user HybridRAG % uv run src/index.py

```

## Full commands

```console
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen3:30b-a3b-instruct-2507-q8_0
ollama pull bge-m3:latest
uv run src/index.py
```
