# Use the Alpine Linux base image
FROM ubuntu:latest

# Update package repository and install necessary packages
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y make gcc libc-dev tcl
RUN apt-get install -y redis

RUN apt-get install -y python3.10-venv
RUN apt-get install -y python3-pip

# Handy for debugging
RUN apt-get install -y vim

# Need for NVM installation and AWS CLI
RUN apt-get install -y curl

# Needed for AWS CLI
RUN apt-get install -y unzip

# Install the AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

# Install Node
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get install -y nodejs
RUN node -v
RUN npm -v

# Copy application files to the container
COPY ./backend /active-statistics/backend
COPY ./frontend /active-statistics/frontend
COPY ./entrypoint.sh /active-statistics

WORKDIR /active-statistics/backend
RUN python3 -m venv .venv
RUN . .venv/bin/activate
RUN pip install -e.

WORKDIR /active-statistics/frontend
RUN npm install
RUN npm run build

WORKDIR /active-statistics

# Doesn't actually expose the port, just lets the user know that when they run docker, this port *should* be exposed.
EXPOSE 3000

CMD ["/bin/bash", "entrypoint.sh"]
