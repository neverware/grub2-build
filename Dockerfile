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
# TODO: branch
RUN git clone -b bishop-grub-fedora33 \
    https://github.com/neverware/chromiumos-grub2.git grub-src

ENV GNULIB_REVISION="d271f868a8df9bbec29049d01e056481b7a1a263"

ADD container/build.py
RUN python3 build.py

WORKDIR grub-src
RUN bash bootstrap

RUN /build/build.py x86_64
RUN /build/build.py i386
