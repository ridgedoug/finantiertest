FROM python:3.8-slim-buster

WORKDIR /program

COPY requirements.txt .

RUN python3.8 -m pip install --upgrade pip && \
    python3.8 -m pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "./app.py"]