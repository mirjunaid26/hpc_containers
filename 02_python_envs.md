# Module 2: Python Environment Management

Managing Python environments in HPC can be challenging due to conflicting dependencies and version requirements. Apptainer solves this by encapsulating the entire environment.

## Strategies for Python

1.  **System Python**: Installing packages directly into `/usr/lib/pythonX.Y` using `pip` (as root during build). Good for small images.
2.  **Conda/Mamba**: Creating a self-contained Conda environment. Preferred for data science as it handles non-Python dependencies (e.g., CUDA toolkits, C libraries).

## Best Practices

-   **Clean up**: Always run `conda clean --all` or `pip cache purge` to keep image size down.
-   **Environment Variables**: Set `PATH` correctly in `%environment` so the container uses your custom Python by default.
-   **Reproducibility**: Use `requirements.txt` or `environment.yml` files.

## Exercise: Building a Data Science Container

In this exercise, we will build a container with a specific version of Python and some common libraries (numpy, pandas) using Conda.

See `exercises/02_conda.def`.

### Key Elements in the Definition File

-   **Base image**: We pull `condaforge/miniforge3` directly from Docker Hub, which already has Conda installed at `/opt/conda` -- no installer script to download in `%post`. (An earlier version of this exercise downloaded the Miniconda installer with `wget` during `%post`; on some HPC login nodes that extra network hop fails under `--fakeroot` even though the base-image pull itself succeeds, so we now start from a pre-built image instead.)
-   **Environment creation**: `conda create -n myenv ...` builds the actual environment in `%post`.
-   **Path Management**: We add the conda env's `bin` directory to `$PATH` in `%environment`.
-   **Self-check**: `%test` verifies the environment with a quick `import numpy`, runnable any time via `apptainer test conda.sif`.

### Running python scripts

Once built, you can run scripts easily:

```bash
apptainer build --fakeroot conda.sif ../02_building/exercises/02_conda.def
apptainer exec conda.sif python script.py
```
