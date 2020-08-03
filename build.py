#!/usr/bin/env python3

import os
import subprocess


def run(*cmd):
    print(' '.join(cmd))
    subprocess.run(cmd, check=True)


def main():
    repo_dir = os.path.dirname(os.path.realpath(__file__))
    output_dir = os.path.join(repo_dir, 'output')

    image = 'grub-build'
    # This revision should match the tip of neverware-fedora33. It is
    # pinned here to ensure the build is reproducible.
    grub_revision = '81e7a8a4c2fa2280de9626739858b5fe5d0b11e2'
    # This revision is newer than what fedora-33 appears to be
    # pointing to (d271f868a8 in a comment in the bootstrap.conf
    # file). We need at least b7e213c072 to pull in a build fix. The
    # newer fixes on top of that (in the fixes branch) are needed to
    # fix some warnings.
    gnulib_revision = '229f262054f003814157c3715a7f33ddfd87d43c'

    # Ensure an empty output directory exists
    run('sudo', 'rm', '-rf', output_dir)
    os.mkdir(output_dir)

    targets = {
        'x86_64': 'grubx64.efi',
        'i386': 'grubia32.efi',
    }

    for target, output_name in targets.items():
        # yapf: disable
        run('docker', 'build',
            '--build-arg', 'GRUB_TARGET=' + target,
            '--build-arg', 'GRUB_REVISION=' + grub_revision,
            '--build-arg', 'GNULIB_REVISION=' + gnulib_revision,
            '--build-arg', 'JOBS=' + str(os.cpu_count()),
            '--tag', image,
            '--file', os.path.join(repo_dir, 'Dockerfile'),
            repo_dir)

        run('docker', 'run',
            '--mount', 'type=bind,src={},dst=/host'.format(output_dir),
            image,
            'cp', '/build/boot.efi', os.path.join('/host', output_name))
        # yapf: enable


if __name__ == '__main__':
    main()
