#!/usr/bin/env python3
"""Package the grub builds and upload to S3."""

import datetime
import os

from build import run, OUTPUT_DIR, REPO_DIR


def main():
    """Package the grub builds and upload to S3."""
    now = datetime.datetime.now()
    tar_name = 'grub-unsigned-{}.tar'.format(now.strftime("%d%m%Y-%H%M%S"))
    tar_path = os.path.join(REPO_DIR, tar_name)
    run('tar', '-C', OUTPUT_DIR, '-cf', tar_path, '.')

    s3_bucket = 'neverware-grub'
    run('aws', 's3', 'cp', tar_path, 's3://{}/{}'.format(s3_bucket, tar_name))


if __name__ == '__main__':
    main()
