import argparse
import os
import subprocess


def run(*cmd):
    print(' '.join(cmd))
    subprocess.run(cmd, check=True)


def main():
    parser = argparse.ArgumentParser(description='build grub2')
    parser.add_argument('target')
    args = parser.parse_args()

    build_dir = os.path.join('/build', 'grub-' + args.target)
    os.mkdir(build_dir)

    # yapf: disable
    configure_args = (
        # These args are copied from the chromiumos grub ebuild:
        # https://chromium.googlesource.com/chromiumos/overlays/chromiumos-overlay/+/94083d19b84e55243e455d06bd6ccd8890821e0d/sys-boot/grub/grub-2.02.ebuild
        '--disable-werror',
	'--disable-grub-mkfont',
	'--disable-grub-mount',
	'--disable-device-mapper',
	'--disable-efiemu',
	'--disable-libzfs',
	'--disable-nls',
        '--program-prefix=',

        # Only build EFI; we use syslinux for legacy boot
        '--with-platform=efi',

        '--prefix', '/build/install'
        '--target=' + target
    )
    # yapf: enable
                             

if __name__ == '__main__':
    main()
