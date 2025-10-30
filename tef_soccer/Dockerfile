FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no--cache--dir -r requirements.txt

COPY ball_possession.py .
COPY gol.py .

CMD [ "true" ]