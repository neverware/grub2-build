import argparse
import subprocess


def run(*cmd):
    print(' '.join(cmd))
    subprocess.run(cmd, check=True)


def main():
    parser = argparse.ArgumentParser(description='build grub2')
    parser.add_argument('target')
    args = parser.parse_args()

    platform = 'efi'
    
    build_dir = os.path.join('/build', 'grub-' + args.target)
    os.mkdir(build_dir)

    # These args are copied from the chromiumos grub ebuild:
    # https://chromium.googlesource.com/chromiumos/overlays/chromiumos-overlay/+/94083d19b84e55243e455d06bd6ccd8890821e0d/sys-boot/grub/grub-2.02.ebuild
    configure_args = [
        '--disable-werror',
	'--disable-grub-mkfont',
	'--disable-grub-mount',
	'--disable-device-mapper',
	'--disable-efiemu',
	'--disable-libzfs',
	'--disable-nls',
	'--sbindir=/sbin',
	'--bindir=/bin',
	'--libdir=/lib64',
	--with-platform=${platform} \
				--target=${target} \
				--program-prefix=
    )
                         

if __name__ == '__main__':
    main()
