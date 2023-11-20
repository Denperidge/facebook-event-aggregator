FROM python:3.10

WORKDIR /src/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "-m", "src.facebook_event_aggregator"]