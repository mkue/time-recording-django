FROM python:3-alpine
MAINTAINER Michael Kündig <michael@minutevideos.com>

ENV PYTHONUNBUFFERED 1

RUN apk update && apk add build-base postgresql-dev git bash
RUN git clone https://github.com/vishnubob/wait-for-it.git /docker

COPY config /config

RUN pip install --upgrade pip
RUN pip install -r /config/requirements.txt

COPY django_root /src
WORKDIR /src

CMD ["/docker/wait-for-it.sh", "db:5432", "--", "bash", "-c", "./run_server"]