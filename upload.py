#!/usr/bin/env python3
"""Upload the tarball to S3."""

import glob
import os

from build import run, OUTPUT_DIR


def main():
    """Upload the tarball to S3."""
    s3_bucket = 'neverware-grub'
    tar_path = glob.glob(os.path.join(OUTPUT_DIR, '*.tar.gz'))[0]
    run('aws', 's3', 'cp', tar_path, 's3://{}/'.format(s3_bucket))


if __name__ == '__main__':
    main()
