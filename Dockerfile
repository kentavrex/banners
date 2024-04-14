FROM  docker-registry.selectel.ru/library/python:3.12

ADD requirements.txt /banners/

WORKDIR /banners

RUN apt-get update  \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && rm requirements.txt

ADD . /banners

EXPOSE 8000

CMD [ "/bin/bash", "start-dev.sh" ]