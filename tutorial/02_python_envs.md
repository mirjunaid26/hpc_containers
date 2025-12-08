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

In this exercise, we will build a container with a specific version of Python and some common libraries (numpy, pandas) using Miniconda.

See `exercises/02_conda.def`.

### Key Elements in the Definition File

-   **Installation**: We download and install Miniconda in `%post`.
-   **Path Management**: We add the conda bin directory to `$PATH` in `%environment`.

### Running python scripts

Once built, you can run scripts easily:

```bash
apptainer exec conda_env.sif python script.py
```
