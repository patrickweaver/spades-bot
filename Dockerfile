FROM ubuntu:16.04

RUN apt-get -yqq update
RUN apt-get -yqq install python-pip python-dev


# Create app directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Bundle app source
ADD . /usr/src/app

# Install app dependencies
ADD requirements.txt /usr/src/app
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "./server.py"]
