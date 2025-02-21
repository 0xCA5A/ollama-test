run_text: env
	OLLAMA_MODEL=llama3.2:1b .venv/bin/python src/text_test.py

run_img: env
	.venv/bin/python src/img_test.py

run_pdf: env
	.venv/bin/python src/pdf_test.py

run_pdf_local_ocr: env
	FILE_PATH=data/eMediplan_de.pdf .venv/bin/python src/pdf_local_ocr_test.py

env:
	python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

format:
	ruff format .

check:
	ruff check .
