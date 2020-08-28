FROM python:3.8.5

ENV LC_ALL="C.UTF-8"
ENV LANG="C.UTF-8"
ENV DEBIAN_FRONTEND="noninteractive"
ENV TZ="Asia/Seoul"
ENV ENV="production"

COPY ./requirements/bot_telegram/requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt

COPY ./main_bot_telegram.py /app/main_bot_telegram.py
COPY ./src/shared /app/src/shared
COPY ./src/configs/settings.py /app/src/configs/settings.py
COPY ./src/bot_telegram /app/src/bot_telegram

WORKDIR /app

ENTRYPOINT ["python3", "main_bot_telegram.py"]
