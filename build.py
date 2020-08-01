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
    # TODO
    grub_branch = 'bishop-grub-fedora33'
    gnulib_revision = 'd271f868a8df9bbec29049d01e056481b7a1a263'

    # yapf: disable
    run('docker', 'build',
        '--build-arg', 'GRUB_BRANCH=' + grub_branch,
        '--build-arg', 'GNULIB_REVISION=' + gnulib_revision,
        '--tag', image,
        '--file', os.path.join(container_dir, 'Dockerfile'),
        container_dir)
    # yapf: enable

    # TODO: other target
    run('docker', 'run', image, 'python3', '-u', '/build/build.py', 'x86_64')


if __name__ == '__main__':
    main()
