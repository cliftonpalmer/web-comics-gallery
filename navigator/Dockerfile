FROM python:3.7-alpine

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_PORT=5000

EXPOSE 5000

RUN apk update

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt

COPY ./app/app.py     /app
COPY ./app/templates/ /app/templates/

CMD ["flask", "run"]
