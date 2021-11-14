FROM python:3.9-alpine

RUN apk add git
RUN pip install virtualenv