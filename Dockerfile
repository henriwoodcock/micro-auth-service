# pull official base image
FROM python:3.10.8-alpine

WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN export LDFLAGS="-L/usr/local/opt/openssl/lib"

# install dependencies
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY docker-entrypoint.sh /usr/src/app/docker-entrypoint.sh
COPY gunicorn.config.py /usr/src/app/gunicorn.config.py

EXPOSE 5000

COPY ./auth_service /usr/src/app/auth_service
RUN ls -la
RUN chmod +x docker-entrypoint.sh
ENTRYPOINT [ "./docker-entrypoint.sh" ]
