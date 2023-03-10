.PHONY: requirements format lint test bump-major bump-minor bump-patch docs

requirements:
	pip install -e .
	pip install -r requirements-dev.txt
	pip install -r requirements-test.txt
	pip install -r requirements.txt

format:
	black dtuhpc/ tests/
	isort dtuhpc/ tests/

lint:
	flake8 dtuhpc/ tests/

test:
	pytest -v tests/
