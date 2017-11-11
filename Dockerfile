FROM ubuntu:16.04

# Create app directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install -y python-pip

# Install app dependencies
ADD requirements.txt /usr/src/app
RUN pip install -r requirements.txt

# Bundle app source
COPY . /usr/src/app

EXPOSE 3000
CMD ["python", "server.py"]
