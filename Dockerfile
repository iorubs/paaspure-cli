FROM python:3-alpine

LABEL maintainer "ruben.vasconcelos3@mail.dcu.ie"

# Update and patch system
RUN apk update \
    && apk add \
      git \
      docker

# TODO: change this to /path once puller is implemented module/component code
# is moved to their own repos
ENV PYTHONPATH /app:/app/paaspure

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
