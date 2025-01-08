FROM selenium/standalone-chrome:131.0

WORKDIR /src/src/app

RUN sudo apt-get update
RUN sudo apt-get install -y git python3 python3-venv

COPY requirements.txt ./
RUN python3 -m venv .venv
RUN .venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [".venv/bin/python3", "-m", "src.facebook_event_aggregator", "--chromedriver-path", "/usr/bin/chromedriver"]