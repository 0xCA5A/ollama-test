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

## Shell hint

``` shell
alias ollama="podman exec -it ollama ollama"
```

Model source: https://ollama.com/search

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

Fetch the models you want to use:

```shell
ollama pull llama3.2:3b
```

```shell
ollama list
```

Prepare the Python environment:

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run tests

```shell
OLLAMA_API_URL=https://external.ollama.ch/api/generate OLLAMA_MODEL=llama3.2-vision:11b FILE_PATH=data/eMediplan_de.pdf make src/pdf_test.py
```

or simply

```shell
make run_text
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
- good aproach if complex data sets are provided
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
