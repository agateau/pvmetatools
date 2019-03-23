FROM ubuntu:18.10

RUN apt-get update --yes \
    && apt-get install --yes --no-install-recommends \
        ffmpeg \
        g++ \
        gcc \
        libboost-python-dev \
        libexiv2-dev \
        locales \
        python3-pip \
        python3-setuptools

RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8

RUN mkdir /src
COPY . /src

RUN pip3 install wheel
RUN pip3 install -r /src/requirements.txt
RUN pip3 install /src

WORKDIR /media
ENTRYPOINT ["bash"]
