FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get install -y python python-setuptools python-dev build-essential python-pip python-mysqldb

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]
