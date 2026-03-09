# Ollama Demos

# Environment Setup

## Ollama

## Start the container

```shell
mkdir -p ${HOME}/ollama

podman run -d \
  -p 11434:11434 \
  --volume ${HOME}/ollama:/root/.ollama \
  --name ollama \
  ollama/ollama
```

## Pull models

```shell
podman exec -it ollama ollama pull deepseek-r1:14b
```

### Anamnesis models

```shell
ollama pull medllama2:7b
ollama pull meditron:7b
ollama pull mistral-small3.1:24b
```

## Shell hint

``` shell
alias ollama="podman exec -it ollama ollama"
```

Model source: https://ollama.com/search

### Remote Ollama

Set `OLLAMA_HOST` to connect to a remote Ollama instance:

```shell
export OLLAMA_HOST=https://ollama.example.com
```

# Ollama Open WebUI

https://docs.openwebui.com/

## Start the container

```shell
mkdir -p ${HOME}/openwebui

podman run -d \
  -p 3000:8080 \
  --volume ${HOME}/openwebui:/app/backend/data \
  -e WEBUI_AUTH=False \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

## Code Setup

Install dependencies with Poetry:

```shell
poetry install
```

Fetch the models you want to use:

```shell
ollama pull llama3.2:3b
```

```shell
ollama list
```

## Run demos

```shell
make run_text
make run_img
make run_pdf
make run_pdf_local_ocr
make run_anamnesis
```

Or with environment overrides:

```shell
OLLAMA_HOST=https://external.ollama.ch make run_pdf
```

## Linting

```shell
make check
make format
```

# Anamnesis CLI

Interactive medical anamnesis analysis tool. Sends a patient anamnesis (German) to a medical LLM and translates the response to German if needed.

Required models:
- `medllama2:7b` or `meditron:7b` (medical analysis)
- `mistral-small3.1:24b` (translation fallback)

```shell
make run_anamnesis
```

# Theory

## Retraining

- like a student sent back to school to improve what he already knows
- fine tune, add to the current knowledge
- a lot of computational work, time consuming
- permanent
- __long term permanent knowledge within the model__

## Retrieval Augmented Generation (RAG)

- like a student not knowing everything but knows exactly where to look; if a question is asked he quickly consults his
  resources (books) and gives a response combined with what he know before and he just looked up
- faster than retraining, does not involve the deep learning of new material
- allows the model to retrieve information dynamically from a database or document pool
- more agile
- __fetches relevant knowledge dynamically without needing to retrain__
- handles a large amount of specific data efficient (memory, processing capacity), pulls only out what is necessary for
  the query
- can refer to dynamically changing sources
- good approach if complex data sets are provided
- more dynamic and scalable approach
- use case for handling large and evolving databases
- responses reflect the most up-to-date information available
- hint: choose smaller base model to be more dependent on your own provided data

## Context Docs

- like a student using a cheat sheet during an exam
- model can reference notes while answering questions
- volatile
- quickest way to provide immediate knowledge
- information lasts as long as the specific session
- __temporary cheat sheet for references__
- uploaded doc content is directly inserted to the models input window
- the model has to deal with all the information provided, even if it is not relevant or not
- search might be limited by the context window size (if a larger amount of documents should be included in the search)
- use case for smaller, more static data sets

Source: https://www.youtube.com/watch?v=fFgyOucIFuk&t=812s
