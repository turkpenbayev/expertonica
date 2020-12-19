# pull official base image
FROM python:3.7-slim

# set work directory
WORKDIR /usr/src/app

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2
# RUN apt-get update \
#     && apt-get install -y build-essential \
#     && apt-get install -y python3-dev\
#     && apt-get install -y libpq-dev

# RUN pip install psycopg2

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# copy project
COPY . /usr/src/app/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
#CMD python manage.py runserver 0.0.0.0:$PORT 
