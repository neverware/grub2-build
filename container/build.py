import argparse
import os
import subprocess


def run(*cmd, cwd=None):
    print(' '.join(cmd))
    subprocess.run(cmd, check=True, cwd=cwd)


def main():
    parser = argparse.ArgumentParser(description='build grub2')
    parser.add_argument('--jobs', type=int, default=os.cpu_count())
    parser.add_argument('target')
    args = parser.parse_args()

    build_dir = os.path.join('/build', 'grub-' + args.target)
    os.mkdir(build_dir)

    # yapf: disable
    run('/build/grub-src/configure',

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

        # Install everything to an isolated prefix
        '--prefix', '/build/install',

        '--target=' + args.target,

        cwd=build_dir)
    # yapf: enable

    run('make', '--jobs', args.jobs, cwd=build_dir)


if __name__ == '__main__':
    main()
