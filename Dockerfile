FROM python:3.8.5

RUN apt-get -y update
RUN pip install --upgrade pip
RUN apt-get -y install ffmpeg

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
# COPY . .

EXPOSE 8000