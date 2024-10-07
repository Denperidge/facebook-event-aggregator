.ONESHELL:
all: .venv install

.venv:
	python -m venv .venv

.PHONY: install
install:
	.venv/bin/pip install -r requirements.txt

.PHONY: install-test
install-test:
	.venv/bin/pip install -r requirements.txt -r requirements-test.txt

.PHONY: test
test:
	.venv/bin/python -m pytest
	.venv/bin/python -m coverage_badge -fo coverage.svg
