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
ARG GRUB_REVISION
RUN git clone \
    https://github.com/neverware/chromiumos-grub2.git \
    grub-src
WORKDIR grub-src

RUN git checkout ${GRUB_REVISION}

ARG GNULIB_REVISION
RUN bash bootstrap

WORKDIR /build/grub-build

ARG GRUB_TARGET
RUN /build/grub-src/configure \
    # These args are copied from the chromiumos grub ebuild:
    # https://chromium.googlesource.com/chromiumos/overlays/chromiumos-overlay/+/94083d19b84e55243e455d06bd6ccd8890821e0d/sys-boot/grub/grub-2.02.ebuild
    --disable-grub-mkfont \
    --disable-grub-mount \
    --disable-device-mapper \
    --disable-efiemu \
    --disable-libzfs \
    --disable-nls \
    --program-prefix= \
    # This flag was added by Fedora in ee5038ddf3b7d91, set it to
    # host to fix missing header errors
    --with-utils=host \
    # Disable the rpm-sort module added by redhat
    --enable-rpm-sort=no \
    # Only build EFI; we use syslinux for legacy boot
    --with-platform=efi \
    # Install everything to an isolated prefix
    --prefix /build/install \
    --target="${GRUB_TARGET}"

ARG JOBS
RUN make "-j${JOBS}"
RUN make install

# These args are copied from upstream:
# https://chromium.googlesource.com/chromiumos/platform/crosutils/+/c2e13fd6594226881b2830e9d6428069fdfa2cee/build_library/create_legacy_bootloader_templates.sh
RUN /build/install/bin/grub-mkimage \
    -O "${GRUB_TARGET}-efi" \
    -o /build/boot.efi \
    -p /efi/boot \
    boot \
    chain \
    configfile \
    efi_gop \
    ext2 \
    fat \
    gptpriority \
    hfs \
    hfsplus \
    linux \
    normal \
    part_gpt \
    test
