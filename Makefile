run_text: env
	OLLAMA_MODEL=llama3.2:1b python3 src/text_test.py

run_img: env
	FILE_PATH=data/bug.jpg python3 src/img_test.py

run_pdf: env
	FILE_PATH=data/eMediplan_de.pdf python3 src/pdf_test.py

run_pdf_local_ocr: env
	FILE_PATH=data/eMediplan_de.pdf python3 src/pdf_test.py

env:
	python3 -m venv .venv && source .venv/bin/activate
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

format:
	ruff format .

check:
	ruff check .
