FROM python:3.9

WORKDIR /docker-flask-app

ADD . /docker-flask-app/

RUN pip3 install -r requirements.txt

EXPOSE 5000


CMD ["python", "app.py" ]

