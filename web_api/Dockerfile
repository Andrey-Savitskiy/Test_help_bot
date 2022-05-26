FROM python:3.9

WORKDIR /web_api
COPY ./web_api/requirements.txt /web_api/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python3", "app.py"]
