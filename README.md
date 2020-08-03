# grub2-build

Note: this repo is public to assist with shim review.

This repo contains tools to prepare a build of GRUB2 for EFI and
upload it to S3.

## Usage

To build, run `./build.py`. This will produce two files in the
`output/` directory: `grubia32.efi` and `grubx64.efi`. A tarball is
created of the two files. The tarball is named with a sha256 hash of
the two files it contains.

To upload to S3, run `./upload.py`. This will upload the tarball
created by `build.py` to the `neverware-grub` bucket (assuming you
have permission to write to that bucket, of course).

Note that the files are unsigned; see the (private)
[cloudready-signing](https://github.com/neverware/cloudready-signing)
repo for details on how to sign grub so that it can be booted via shim
with secure boot enabled.

## TODO

Describe details of where the sources come from and what patches
we apply on top.
