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

.PHONY: docker-build
docker-build:
	sudo docker build -t fae . --no-cache

.PHONY: docker-run
docker-run:
	sudo docker run --shm-size="2g" fae --host-domain https://concerts.neonpastel.net --repo https://github.com/Denperidge-Friends/belgian-concerts.git --scrape --update --target https://www.facebook.com/trixonline/