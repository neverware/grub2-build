FROM fedora:32

# redhat-rpm-config is needed here because of a2956cf47d in the redhat
# gnulib repo. This in turn implies that we need to use a fedora image
# rather than, say, debian-slim.
RUN dnf install -y \
    autoconf \
    automake \
    bison \
    flex \
    gettext-devel \
    git \
    libtool \
    make \
    pkg-config \
    python3 \
    redhat-rpm-config

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
