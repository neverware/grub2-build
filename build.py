#!/usr/bin/env python3
"""Build grub for EFI."""

import hashlib
import os
import subprocess

REPO_DIR = os.path.dirname(os.path.realpath(__file__))
OUTPUT_DIR = os.path.join(REPO_DIR, 'output')


def run(*cmd):
    """Print and run a command via subprocess."""
    print(' '.join(cmd))
    subprocess.run(cmd, check=True)


def main():
    """Build grub for EFI."""
    image = 'grub-build'
    # This revision should match the tip of neverware-fedora33. It is
    # pinned here to ensure the build is reproducible.
    grub_revision = 'e37e9ced05e7406b60ef8df401126f0c65de4399'
    # This revision is newer than what fedora-33 appears to be
    # pointing to (d271f868a8 in a comment in the bootstrap.conf
    # file). We need at least b7e213c072 to pull in a build fix. The
    # newer fixes on top of that (in the fixes branch) are needed to
    # fix some warnings.
    gnulib_revision = '229f262054f003814157c3715a7f33ddfd87d43c'

    # Ensure an empty output directory exists
    run('sudo', 'rm', '-rf', OUTPUT_DIR)
    os.mkdir(OUTPUT_DIR)

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
            '--file', os.path.join(REPO_DIR, 'Dockerfile'),
            REPO_DIR)

        run('docker', 'run',
            '--mount', 'type=bind,src={},dst=/host'.format(OUTPUT_DIR),
            image,
            'cp', '/build/boot.efi', os.path.join('/host', output_name))
        # yapf: enable

    # Hash the outputs in sorted order to produce a stable hash
    hasher = hashlib.sha256()
    for file_name in sorted(targets.values()):
        with open(os.path.join(OUTPUT_DIR, file_name), 'rb') as rfile:
            hasher.update(rfile.read())

    # Create a tarball of the outputs
    tar_name = 'grub-unsigned-{}.tar.gz'.format(hasher.hexdigest())
    tar_path = os.path.join(OUTPUT_DIR, tar_name)
    tar_cmd = ['tar', '-C', OUTPUT_DIR, '-czvf', tar_path]
    tar_cmd += targets.values()
    run(*tar_cmd)


if __name__ == '__main__':
    main()
