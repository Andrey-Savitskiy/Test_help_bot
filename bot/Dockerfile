FROM python:3.9

WORKDIR /bot
COPY ./requirements.txt /bot/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
COPY . /bot
CMD ["python3", "main.py"]
