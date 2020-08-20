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

## Modifications to grub2

The version of grub2 we build is based off of the RedHat fork:
https://github.com/rhboot/grub2/tree/fedora-33

We require a few additional changes on top of that, so we have our own
fork, currently based on the `fedora-33` branch of RedHat's fork:
https://github.com/neverware/grub2

See `build.py` for the exact commit we build from.

Here is a list of the changes we apply:

- Two patches from the `master` branch of the upstream GNU repo
  (http://git.savannah.gnu.org/gitweb/?p=grub.git) to fix warnings:

  ```bash
  # mdraid1x_linux: Fix gcc10 error -Werror=array-bounds)
  git cherry-pick -x bdf170d1018a500a7fea8d43677c5b4fc8812c74
  # zfs: Fix gcc10 error -Werror=zero-length-bounds
  git cherry-pick -x 68006d173291c6e972c4882d4fa40dc91a9c1d45
  ```
- Two patches from ChromiumOS:
  https://chromium.googlesource.com/chromiumos/overlays/chromiumos-overlay/+/3d20670d426f9e1864e8d87fe2344770ff09614a/sys-boot/grub/files/
  - `0001-Forward-port-ChromeOS-specific-GRUB-environment-vari.patch`
  - `0002-Forward-port-gptpriority-command-to-GRUB-2.00.patch`

  Apply those patches with `git am`.
- A patch to fix compilation with rpm-sort disabled:
  https://github.com/rhboot/grub2/pull/46

  ```bash
  git cherry-pick -x 190bcfa261b5cbf309fc144f1a58d5917a311632
  ```
- And a couple Neverware-authored patches to fix warnings:
  - `fbbdb83a8874cf808faae7a62643cb936986dd08` (Fix a sign-compare warning)
  - `e37e9ced05e7406b60ef8df401126f0c65de4399` (Fix compilation warnings on 32-bit)

## TODO

- Check if any modules in the call to grub-mkimage can be dropped.
