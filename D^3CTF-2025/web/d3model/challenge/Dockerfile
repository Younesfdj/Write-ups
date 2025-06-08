FROM python:3.10-slim

COPY app.py /app/app.py
COPY requirements.txt /app/requirements.txt
COPY index.html /app/index.html
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

ENV FLAG=${FLAG:-flag{test}}

EXPOSE 5000

CMD ["python", "app.py"]
