FROM python:3.9

WORKDIR /coupon-api

ADD /coupon-api /coupon-api/

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python", "coupon-api.py" ]
