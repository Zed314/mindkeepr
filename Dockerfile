FROM python:latest

ENV PROD True

RUN mkdir /code

WORKDIR /code
RUN mkdir /code/MindkeeprMain
ADD ./MindkeeprMain/ /code/MindkeeprMain
ADD ./fixtures/ /code/fixtures
RUN mkdir /code/Mindkeepr
ADD ./Mindkeepr/ /code/Mindkeepr
RUN mkdir /code/templates
ADD ./templates/ /code/templates
COPY ./manage.py /code/
COPY ./requirements.txt /code/
COPY ./.env.dev /code/
COPY ./.env.prod /code/
COPY ./entrypoint.sh /code/
RUN chmod u+x /code/entrypoint.sh
RUN mkdir /code/static
RUN mkdir /code/media
RUN mkdir /code/backup

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y netcat
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN python manage.py loaddata fixtures/initdata.json
RUN python manage.py loaddata fixtures/moviegenre.json
EXPOSE 80

ENTRYPOINT ["/code/entrypoint.sh"]