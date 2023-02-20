FROM python:3.8-alpine
RUN apk add -u gcc musl-dev

WORKDIR /backend

VOLUME /db
COPY ./db /db
COPY . /backend

RUN pip3 install -r requirements.txt

EXPOSE 8000

