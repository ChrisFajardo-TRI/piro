# syntax=docker/dockerfile1
ARG VERSION=18.04
FROM ubuntu:$VERSION
ENV USERNAME dev
# Insert your generated `pymatgen` API key below in place of
# `insert-api-key-here` before building
ENV MP_API_KEY insert-api-key-here
WORKDIR /home/$USERNAME

COPY . ./piro/

RUN apt-get update \
 && apt-get -y update \
 && apt-get install -y \
    software-properties-common \
    build-essential \
    git \
 && apt-get clean -qq

RUN add-apt-repository ppa:deadsnakes/ppa

RUN apt-get update \
 && apt-get -y update \
 && apt-get install -y \
    python3.7 \
    python3.7-dev \
    python3-pip \
 && apt-get clean -qq

RUN python3.7 -m pip install --upgrade \
    pip \
    setuptools \
    wheel

RUN python3.7 -m pip install --upgrade \
    numpy \
    Cython \
    jupyter \
    pymatgen \
    matminer \
    joblib \
    scipy \
    threadpoolctl \
    pytz

WORKDIR /home/$USERNAME/piro/

RUN python3.7 setup.py develop
