FROM python:3.9

WORKDIR /web

COPY . .
COPY requirements.txt .

RUN pip3 install -r requirements.txt

EXPOSE 5000


CMD ["python", "app.py" ]

