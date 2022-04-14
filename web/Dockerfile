FROM python:3.9

WORKDIR /web

COPY . .

RUN pip3 install -r web/requirements.txt

EXPOSE 5000


CMD ["python", "app.py" ]

