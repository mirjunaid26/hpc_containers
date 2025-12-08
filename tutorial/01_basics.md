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

### Building (Requires Root)

*Note: Building usually requires root access. If you are on an HPC cluster, you might need to build on your laptop or use the `--remote` builder feature.*

```bash
sudo apptainer build hello.sif exercises/01_hello.def
```
