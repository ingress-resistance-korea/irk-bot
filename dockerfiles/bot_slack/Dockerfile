FROM python:3.8.5

ENV LC_ALL="C.UTF-8"
ENV LANG="C.UTF-8"
ENV DEBIAN_FRONTEND="noninteractive"
ENV TZ="Asia/Seoul"
ENV ENV="production"

COPY ./requirements/bot_slack/requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt

COPY ./main_bot_slack.py /app/main_bot_slack.py
COPY ./src/shared /app/src/shared
COPY ./src/configs/settings.py /app/src/configs/settings.py
COPY ./src/bot_slack /app/src/bot_slack

WORKDIR /app

ENTRYPOINT ["python3", "main_bot_slack.py"]
