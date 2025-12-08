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
