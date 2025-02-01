run_text: env
	pipenv run python3.10 text_test.py

env:
	pipenv install

check:
	ruff check .
