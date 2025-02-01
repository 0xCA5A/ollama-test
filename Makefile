run_text: env
	pipenv run python3.10 text_test.py

run_img: env
	pipenv run python3.10 img_test.py

env:
	pipenv install

format:
	ruff format .

check:
	ruff check .
