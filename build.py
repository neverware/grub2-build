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
    # TODO: might want to pin this to a particular commit and leave
    # the branch name in a comment
    grub_branch = 'neverware-fedora33'
    # This revision is newer than what fedora-33 appears to be
    # pointing to (d271f868a8 in a comment in the bootstrap.conf
    # file). We need at least b7e213c072 to pull in a build fix. There
    # are some newer fixes on top of that (in the fixes branch) but
    # they introduce new compilation errors.
    gnulib_revision = 'b7e213c072670ca78ebcdcc4853ece9c2452ee82'

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
