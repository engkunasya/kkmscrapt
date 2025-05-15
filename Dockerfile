FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y \
    wget curl unzip fonts-liberation libnss3 libxss1 libasound2 libatk1.0-0 libatk-bridge2.0-0 libgtk-3-0 libgbm1 \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

CMD ["python", "cloud.py"]
