FROM ubuntu:18.04

ENV LC_ALL="C.UTF-8"
ENV LANG="C.UTF-8"
ENV DEBIAN_FRONTEND="noninteractive"
ENV TZ="Asia/Seoul"

COPY binaries/google-chrome-stable_current_amd64.deb /app/binaries/google-chrome-stable_current_amd64.deb
COPY binaries/chromedriver /app/binaries/chromedriver

RUN apt-get update && apt-get autoremove && apt-get autoclean \
    && apt-get install -y \
        tzdata \
        python3-pip \
        build-essential \
        libxss1 \
        libgconf2-4 \
        libappindicator1 \
        libindicator7 \
        fonts-liberation \
        libasound2 \
        libnspr4 \
        libnss3 \
        libx11-xcb1 \
        wget \
        xdg-utils \
        libappindicator3-1 \
        libatk-bridge2.0-0 \
        libatspi2.0-0 \
        libgtk-3-0 \
    && dpkg -i /app/binaries/google-chrome-stable_current_amd64.deb \
    && rm -rf /var/lib/apt/lists/*
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY requirements/worker/requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt

COPY main_worker.py /app/main_worker.py
COPY src/configs /app/src/configs
COPY src/worker /app/src/worker
COPY src/shared /app/src/shared

RUN chmod +x /app/binaries/chromedriver \
    && mkdir -p /app/screenshots
 
WORKDIR /app

ENTRYPOINT ["python3", "main_worker.py"]
