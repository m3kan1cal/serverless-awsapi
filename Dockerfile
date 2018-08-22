FROM amazonlinux

# Make able to install Node 8.x from upstream.
# Install Python3.6 with pip and devel.
# Install GCC, Make and MySQL-devel, NodeJS, Nano, findutils, and libyaml for parsing .yml (serverless) via Python.
# Clean-up after ourselves.
RUN curl --silent --location https://rpm.nodesource.com/setup_8.x | bash - && \
  yum install -y python36-pip python36-devel gcc-c++ make mysql-devel && \
  nodejs vim findutils libyaml libyaml-devel git && \
  yum clean all

# Install/upgrade pipenv, pip, awscli, mysqlclient for Python 3.6.
RUN pip-3.6 install --no-cache-dir --upgrade pipenv pip awscli mysqlclient pyyaml

# Install the serverless framework globally.
RUN npm install -g serverless

# Set environment vars.
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV APP_ROOT /app

WORKDIR ${APP_ROOT}

# -- Install dependencies:
ONBUILD RUN set -ex && pipenv install --deploy --system

# Set our entrypoint for usable Serverless prompt.
ENTRYPOINT ["/bin/bash", "-c"]
