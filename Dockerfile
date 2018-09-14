# Getting started, use the following steps.
# To build (at command line): docker image build -t stoictechgroup/stoic-serverless-awsapi .
# To run (at command line):
# AWS_ACCESS_KEY_ID=$(aws --profile YOUR_PROFILE configure get aws_access_key_id)
# AWS_SECRET_ACCESS_KEY=$(aws --profile YOUR_PROFILE configure get aws_secret_access_key)
# docker container run -v "$(pwd)":/app -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY -d stoictechgroup/stoic-serverless-awsapi
FROM ubuntu:18.04

# Install Python 3.6 and dependencies.
RUN apt-get update && apt-get upgrade -y && \
  apt-get install -y build-essential python3.6 python3.6-dev python3-pip curl && \
  curl -sL https://deb.nodesource.com/setup_8.x | bash - && \
  apt-get install -y nodejs

RUN python3.6 -m pip install pip awscli pipenv --upgrade

# Set environment variables.
ENV AWS_ACCESS_KEY_ID ""
ENV AWS_SECRET_ACCESS_KEY ""

ENV DYNAMODB_HOST https://dynamodb.us-west-2.amazonaws.com
ENV DYNAMODB_TABLE stoic-notes-dev
ENV DYNAMODB_GSI_USERID_NOTEID stoic-notes-dev-userid-noteid-index
ENV DYNAMODB_GSI_NOTEBOOK_NOTEID stoic-notes-dev-notebook-noteid-index

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# Set working directory, assume volume has 
# been passed on command line.
ENV APP_ROOT /app
WORKDIR ${APP_ROOT}

# Copy over asset files.
COPY ./package.json ./
COPY ./package-lock.json ./
COPY ./Pipfile ./
COPY ./Pipfile.lock ./

# Install project dependencies.
RUN npm i && npm i -g serverless && pipenv install --system --deploy

# Set our entrypoint for usable Serverless prompt.
ENTRYPOINT ["/bin/bash", "-c"]
