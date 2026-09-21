# Module 3: Advanced Definition Files

The definition file (`.def`) is the heart of reproducible container builds. This module explores its advanced sections.

## Key Sections

### %setup
Runs on the **host** system (or inside a preliminary container) before the base OS is installed. Useful for preparing files on the host that need to be copied in.

### %files
Copies files from the host to the container.
```singularity
%files
    requirements.txt /opt/app/
    src/ /opt/app/src/
```

### %environment
Sets environment variables that are available **at runtime** (when you run `apptainer shell` or `exec`).
*Note: These are NOT available during the `%post` build section.*

### %post
Measurements script where you install software. Runs inside the container.

### %startscript
Defines a command that runs when the container instance is started (similar to a service).

## Multi-stage Builds
Apptainer supports multi-stage builds to keep images small. You can build in one stage and copy artifacts to another.

```singularity
Bootstrap: docker
From: golang:1.18 as builder
%post
    # compilation steps

Bootstrap: docker
From: alpine:latest
%files from builder
    /go/bin/app /usr/local/bin/app
```

## Exercise: The All-in-One Container

Examine `exercises/03_complex.def`. It demonstrates:
1.  Copying local scripts.
2.  Setting runtime variables.
3.  Defining labels and help text.

### Two things we had to fix after testing on JURECA

-   **Base image**: the original version used `ubuntu:20.04` and failed under `--fakeroot` with `` GLIBC_2.33'/`2.34' not found `` while Apptainer tried to start its injected `faked` helper. See the note in Module 1 for the general explanation (accounts not in `/etc/subuid` fall back to a fakeroot emulation that needs a reasonably modern glibc in the base image). Switching to `ubuntu:22.04` fixed it.
-   **`%startscript`**: it calls `nc -l -p $APP_PORT -e /bin/cat`, which needs the `-e` flag. Installing the ambiguous `netcat` package on Ubuntu resolves to `netcat-openbsd`, which is compiled *without* `-e` (a deliberate Debian/Ubuntu security choice). This exercise now installs `netcat-traditional` explicitly instead, which keeps `-e` working.

```bash
apptainer build --fakeroot complex.sif ../02_building/exercises/03_complex.def
apptainer test complex.sif
apptainer instance start complex.sif complex_test
apptainer instance stop complex_test
```
