FROM python:3

ENV MICRO_SERVICE=/home/app/

RUN apt-get update && \
    apt-get install -y docker.io

# RUN apk update && apk add python3-dev gcc libc-dev

# where the code lives
WORKDIR $MICRO_SERVICE

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install dependencies
RUN pip install --upgrade pip
# copy project
COPY . .

RUN pip install -r requirements.txt
