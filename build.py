#!/usr/bin/env python3

import os
import subprocess


def run(*cmd):
    print(' '.join(cmd))
    subprocess.run(cmd, check=True)


def main():
    repo_dir = os.path.dirname(os.path.realpath(__file__))
    container_dir = os.path.join(repo_dir, 'container')

    image = 'grub-build'
    # This revision should match the tip of neverware-fedora33. It is
    # pinned here to ensure the build is reproducible.
    grub_revision = '1dbbd0d0003ff5ed2082ee632e46aa3135b5d925'
    # This revision is newer than what fedora-33 appears to be
    # pointing to (d271f868a8 in a comment in the bootstrap.conf
    # file). We need at least b7e213c072 to pull in a build fix. The
    # newer fixes on top of that (in the fixes branch) are needed to
    # fix some warnings.
    gnulib_revision = '229f262054f003814157c3715a7f33ddfd87d43c'

    # yapf: disable
    run('docker', 'build',
        '--build-arg', 'GRUB_REVISION=' + grub_revision,
        '--build-arg', 'GNULIB_REVISION=' + gnulib_revision,
        '--tag', image,
        '--file', os.path.join(container_dir, 'Dockerfile'),
        container_dir)
    # yapf: enable

    for target in ('x86_64', 'i386'):
        run('docker', 'run', image, 'python3', '-u', '/build/build.py', target)


if __name__ == '__main__':
    main()
