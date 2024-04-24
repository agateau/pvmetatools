FROM ubuntu:20.04

RUN apt-get update --yes \
    && apt-get install --yes --no-install-recommends \
        ffmpeg \
        g++ \
        gcc \
        libboost-python-dev \
        libexiv2-dev \
        locales \
        python3-pip

RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8

RUN mkdir /src
COPY . /src
WORKDIR /src
RUN pip install .

WORKDIR /media
ENTRYPOINT ["bash"]
