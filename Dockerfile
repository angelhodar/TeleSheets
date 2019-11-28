FROM python:3.7

LABEL maintainer="Ángel Hódar (angelhodar76@gmail.com)"

COPY requirements.txt /tmp
RUN cd /tmp && pip install -r requirements.txt

COPY telesheets /app/telesheets/
COPY bot.py /app
WORKDIR /app

CMD python bot.py