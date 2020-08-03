# grub-build

Note: this repo is public to assist with shim review.

This repo contains tools to prepare a build of GRUB2 for EFI and
upload it to S3.

To build, run `./build.py`. This will produce two files in the
`output/` directory: `grubia32.efi` and `grubx64.efi`.

To upload to S3, run `./upload.py`. This will tar the two `.efi` files
and upload them to the `neverware-grub` bucket (assuming you have
permission to write to that bucket, of course).

Note that the files are unsigned; see the
[cloudready-signing](https://github.com/neverware/cloudready-signing)
repo for details on how to sign grub so that it can be booted via shim
with secure boot enabled.

TODO: describe details of where the sources come from and what patches
we apply on top.
