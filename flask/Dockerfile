FROM python:3.8.0-slim

RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean

WORKDIR /app 

COPY . /app 

RUN pip install -r requirements.txt 

CMD ["uwsgi","app.ini"]