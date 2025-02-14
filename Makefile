run_text: env
	pipenv run python3.10 src/text_test.py

run_img: env
	FILE_PATH=data/bug.jpg pipenv run python3.10 src/img_test.py

run_pdf: env
	LD_LIBRARY_PATH=$(shell find /nix/ -name "libstdc++.so.6" | head -n 1 | xargs dirname) FILE_PATH=data/eMediplan_de.pdf pipenv run python3.10 src/pdf_test.py

run_pdf_local_ocr: env
	LD_LIBRARY_PATH=$(shell find /nix/ -name "libstdc++.so.6" | head -n 1 | xargs dirname) FILE_PATH=data/eMediplan_de.pdf pipenv run python3.10 src/pdf_test.py

env:
	pipenv install

format:
	ruff format .

check:
	ruff check .
