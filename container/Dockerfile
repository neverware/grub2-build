FROM debian:10.4-slim

ARG GRUB_BRANCH
ARG GNULIB_REVISION

# Note: librpm-dev is needed because the "--enable-rpm-sort=no"
# configure flag does not properly disable the rpm-sort module.
RUN apt-get update && apt-get install -y \
    autoconf \
    automake \
    autopoint \
    bison \
    flex \
    gettext \
    git \
    librpm-dev \
    libtool \
    make \
    pkg-config \
    python3

WORKDIR /build
RUN git clone -b $GRUB_BRANCH \
    https://github.com/neverware/chromiumos-grub2.git \
    grub-src

WORKDIR grub-src
RUN bash bootstrap

ADD build.py /build/
