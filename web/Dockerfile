FROM python:3.9

WORKDIR /web

ADD /web /web/

RUN pip3 install -r requirements.txt

EXPOSE 8082


CMD ["python", "app.py" ]

