install:
	pip install -r requirements.txt

install-test:
	pip install -r requirements.txt requirements-test.txt

test:
	pytest
	python -m coverage_badge -fo coverage.svg