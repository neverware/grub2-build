FROM debian:10.4-slim

RUN apt-get update && apt-get install -y \
    autoconf \
    automake \
    autopoint \
    bison \
    flex \
    gettext \
    git \
    libtool \
    make \
    pkg-config \
    python3

ARG GRUB_BRANCH
ARG GNULIB_REVISION

WORKDIR /build
RUN git clone -b $GRUB_BRANCH \
    https://github.com/neverware/chromiumos-grub2.git \
    grub-src

WORKDIR grub-src
RUN bash bootstrap

ADD build.py /build/
