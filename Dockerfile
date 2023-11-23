FROM seleniarm/standalone-firefox:latest

WORKDIR /src/src/app

RUN sudo apt-get update
RUN sudo apt-get install -y git python3.11 python3-pip

COPY requirements.txt ./
RUN python3.11 -m pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python3.11", "-m", "src.facebook_event_aggregator"]