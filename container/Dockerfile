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

WORKDIR /build
RUN git clone \
    https://github.com/neverware/chromiumos-grub2.git \
    grub-src
WORKDIR grub-src

ARG GRUB_REVISION
RUN git checkout $GRUB_REVISION

ARG GNULIB_REVISION
RUN bash bootstrap

ADD build.py /build/
