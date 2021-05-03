FROM python:3.6-alpine

WORKDIR /flask_docker

RUN apk add git gcc python3-dev gpgme-dev libc-dev
COPY flask_docker/requirements.txt flask_docker/requirements.txt
RUN pip install -r flask_docker/requirements.txt
COPY . /flask_docker

EXPOSE 5011

CMD ["python", "flask_docker/flask_docker.py"]
