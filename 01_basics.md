# Module 1: Basics & Fundamentals

## Why Apptainer in HPC?

Unlike Docker, which runs as a root daemon, Apptainer is designed for secure, user-space execution. This makes it the standard for HPC centers where users do not have root privileges.

Key differences:
- **Security**: You are the same user inside the container as outside.
- **Image Format**: Images are single files (`.sif`), making them easy to move, archive, and share.
- **Integration**: Designed to work seamlessly with resource managers (Slurm, PBS) and specialized hardware (Infiniband, GPUs).

## Exercise 1: From Docker to Apptainer

One of the most common workflows is converting an existing Docker image to Apptainer.

### Pulling from Docker Hub

You can pull directly from Docker Hub. Apptainer effectively converts the layers into a SIF file.

```bash
apptainer pull ubuntu.sif docker://ubuntu:22.04
```

### Running Containers

- **Shell**: Interactive access
  ```bash
  apptainer shell ubuntu.sif
  ```
- **Exec**: Run a specific command
  ```bash
  apptainer exec ubuntu.sif cat /etc/os-release
  ```
- **Run**: Execute the default runscript (entrypoint)
  ```bash
  apptainer run ubuntu.sif
  ```

## Exercise 2: Building your first Image

In the `exercises/` folder, look at `01_hello.def`. This is a definition file, the "recipe" for building an image.

### Building (Requires Root, or `--fakeroot`)

*Note: Building normally requires root access. Most HPC login nodes don't give you that, but Apptainer's unprivileged `--fakeroot` mode works on many systems without any admin involvement -- this is what the exercises in this repo use. If `--fakeroot` isn't available or reliable on your system, fall back to building on your own laptop (where you do have root) and transferring the resulting `.sif` with `scp`, or use the `--remote` builder feature.*

*One thing worth knowing about `--fakeroot` on systems where your account isn't listed in `/etc/subuid` (check with `grep $USER /etc/subuid` -- JURECA is like this): Apptainer can't set up a real unprivileged user namespace, so it falls back to a userspace fakeroot emulation that injects a host-compiled `faked` binary into the container. That fallback has bitten us two different ways while testing this repo on JURECA:*

*1. An Alpine-based image (`apk`, musl libc) failed DNS resolution inside `%post`, even though the base-image pull itself succeeded.*
*2. An `ubuntu:20.04` image failed with `` GLIBC_2.33' not found ``/`` GLIBC_2.34' not found `` while starting the injected `faked` binary, because 20.04's glibc (2.31) was older than what that binary needs.*

*Both were fixed the same way: use a newer glibc-based image. `ubuntu:22.04` and later, or Debian-bookworm-based images, clear the bar -- see `01_hello.def` and `03_complex.def`. If you hit either symptom, try a newer Debian/Ubuntu base before assuming your site blocks builds entirely.*

```bash
apptainer build --fakeroot hello.sif ../exercises/01_hello.def
```
