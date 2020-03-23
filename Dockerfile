# This is a simple Dockerfile to use while developing
# It's not suitable for production
#
# for flask: docker run --env-file=.flaskenv image flask run
#
FROM python:3.7

RUN mkdir /code
WORKDIR /code

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY words words/

EXPOSE 5000
CMD ["flask", "run"]
