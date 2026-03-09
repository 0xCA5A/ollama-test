run_text:
	OLLAMA_MODEL=llama3.2:1b poetry run python src/text_test.py

run_img:
	poetry run python src/img_test.py

run_pdf:
	poetry run python src/pdf_test.py

run_pdf_local_ocr:
	FILE_PATH=data/eMediplan_de.pdf poetry run python src/pdf_local_ocr_test.py

run_anamnesis:
	poetry run anamnesis

format:
	poetry run ruff format .

check:
	poetry run ruff check .
