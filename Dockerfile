FROM zenika/alpine-chrome:124-with-chromedriver
#FROM selenium/standalone-chrome:4.27.0-20250101
WORKDIR /src/src/app

USER root
RUN apk update
#RUN sudo apt-get update
#RUN sudo apt-get install -y git python3 python3-venv
RUN apk add git python3 py3-virtualenv

USER chrome

COPY requirements.txt ./

RUN python3 -m venv .venv
RUN .venv/bin/pip install --no-cache-dir -r requirements.txt



COPY . .

ENTRYPOINT [".venv/bin/python3", "-m", "src.facebook_event_aggregator", "--chromedriver-path", "chromedriver"]