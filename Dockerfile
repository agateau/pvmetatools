#
# Install packages required by both the build and the final images
#
FROM ubuntu:22.04 as base

RUN apt-get update --yes \
    && apt-get install --yes --no-install-recommends \
        python3 \
        libboost-python1.74.0 \
        libexiv2-27

#
# Image used to build and install dependencies
#
FROM base as build

RUN apt-get install --yes --no-install-recommends \
    curl \
    g++ \
    gcc \
    libboost-python-dev \
    libexiv2-dev \
    python3-pip \
    python3-venv \
    xz-utils

# Install ffmpeg
RUN mkdir /opt/ffmpeg \
    && cd /opt/ffmpeg \
    && curl -L https://johnvansickle.com/ffmpeg/old-releases/ffmpeg-6.0.1-amd64-static.tar.xz \
        | tar --strip-components 1 -x --xz

# Install pvmetatools & its dependencies
COPY pvmetatools /src/pvmetatools
COPY pyproject.toml /src
WORKDIR /
RUN python3 -m venv /venv
RUN /venv/bin/python -m pip install /src

#
# The final image
#
FROM base as pvmetatools

RUN apt-get install --yes --no-install-recommends \
    locales

RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8

COPY --from=build /src /src
COPY --from=build /opt/ffmpeg /opt/ffmpeg
COPY --from=build /venv /venv
ENV PATH=/venv/bin:/opt/ffmpeg:$PATH

WORKDIR /media
ENTRYPOINT ["bash"]

#
# Image to run tests
#
FROM pvmetatools as pvmetatools-tests

RUN apt-get install --yes --no-install-recommends \
    python3-pip

COPY requirements-dev.txt /src

WORKDIR /src
RUN /venv/bin/python -m pip install -r requirements-dev.txt

ENTRYPOINT ["bash"]
