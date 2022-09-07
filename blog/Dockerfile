FROM python:3.6

WORKDIR /var/lib/app
ADD ./requirements.txt /var/lib/app

RUN pip install -r requirements.txt

COPY ./app /var/lib/app