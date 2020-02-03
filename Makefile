.PHONY: docs

init:
	pip install poetry
	poetry install

reinit:
	poetry env remove python
	make init

test:
	poetry run pytest

docs:
	cd docs && poetry run make html
