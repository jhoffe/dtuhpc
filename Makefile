requirements:
	pip install -e .
	pip install -r requirements.txt

format:
	black dtuhpc/ tests/
	isort dtuhpc/ tests/

lint:
	flake8 dtuhpc/ tests/

test:
	pytest -v tests/**/*.py