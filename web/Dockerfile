FROM python:3.9

WORKDIR /web

ADD /web /web/

RUN pip3 install -r web/requirements.txt

EXPOSE 5000


CMD ["python", "app.py" ]

