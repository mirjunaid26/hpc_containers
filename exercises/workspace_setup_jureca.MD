# Where to Work, and Keeping Your Apptainer Cache Off `$HOME` (Quota: 5 GB)

Your JURECA home directory quota is only **5 GB**. Every `apptainer pull` or
`apptainer build` downloads image layers into `$HOME/.apptainer/cache` by
default — two or three pulls and you can blow through the whole quota,
which then breaks unrelated things (SSH logins, `.bashrc`, everything that
lives in home).

Fix it once, before you pull your first image, with two environment
variables.

## Where to Do Your Exercises & Build Containers

The shared course material lives at `$PROJECT_training2638/container-workshop/`:

```
$PROJECT_training2638/container-workshop/
├── 01_interacting/     <- shared, read-only reference material
├── 02_building/        <- shared, read-only reference material
├── 03_running_on_hpc/  <- shared, read-only reference material
├── ngc_pytorch.sif     <- pre-staged 10 GB NGC image (see tip below)
└── <your-username>/    <- YOUR personal work area
```

Do all your own work — building images, running exercises, storing
`.sif` files — inside `$PROJECT_training2638/container-workshop/$USER/`,
**not** in `01_interacting/`, `02_building/`, or `03_running_on_hpc/`
(those are shared reference material for everyone) and **not** in
`$HOME` (5 GB quota) or `/p/scratch` (periodically purged — don't risk
losing a container you just spent time building).

```bash
mkdir -p $PROJECT_training2638/container-workshop/$USER

apptainer build \
  $PROJECT_training2638/container-workshop/$USER/my_image.sif \
  my_image.def
```

## Quick Fix: Redirect the Apptainer Cache (do this first)

```bash
mkdir -p $PROJECT_training2638/container-workshop/$USER/apptainer_cache
mkdir -p $PROJECT_training2638/container-workshop/$USER/apptainer_tmp

echo 'export APPTAINER_CACHEDIR=$PROJECT_training2638/container-workshop/$USER/apptainer_cache' >> ~/.bashrc
echo 'export APPTAINER_TMPDIR=$PROJECT_training2638/container-workshop/$USER/apptainer_tmp' >> ~/.bashrc

source ~/.bashrc
```

Keeping it under `container-workshop/$USER/` (rather than directly under
the project root) keeps your cache alongside the rest of the course
material, instead of scattered at the top level of shared project storage.

Verify it's active:

```bash
echo $APPTAINER_CACHEDIR
apptainer cache list
```

That's it — every future pull/build now writes to project storage
instead of home. No symlink needed; the environment variables take
priority over the default `$HOME/.apptainer` location.

> **Tip:** for the NGC PyTorch exercises, a `ngc_pytorch.sif` is already
> staged at `$PROJECT_training2638/container-workshop/ngc_pytorch.sif`.
> You don't need to `apptainer pull` your own copy — that image alone is
> 10 GB, twice your entire home quota.

## Check Your Current Usage

```bash
du -sh $HOME
apptainer cache list
```

If `$HOME` is already close to 5 GB, see the next section.

## If You Already Filled Up `$HOME`

If you pulled images *before* setting the variables above, the data is
sitting in `$HOME/.apptainer/cache`. Move it across (don't just delete
it — you'd have to re-download everything):

```bash
mkdir -p $APPTAINER_CACHEDIR
rsync -av $HOME/.apptainer/cache/ $APPTAINER_CACHEDIR/

# confirm the sizes match before deleting anything
du -sh $HOME/.apptainer/cache
du -sh $APPTAINER_CACHEDIR
```

Only once both sizes match:

```bash
rm -rf $HOME/.apptainer/cache
apptainer cache list   # should report the same totals as before
```

## Common Mistakes to Avoid

- **Single quotes block variable expansion.** `export VAR='$PROJECT_training2638/...'`
  writes the literal text `$PROJECT_training2638` into the path instead of
  its value. Always use double quotes or no quotes at all when a `$VAR` is
  involved.
- **Trailing slashes matter with `rsync`/`mv`.** `source/` copies the
  *contents* of a folder; `source` (no trailing slash) can copy/move the
  whole folder one level deeper than you meant if the destination already
  exists as a directory.
- **Let large transfers finish.** Closing your terminal or hitting
  <kbd>Ctrl-C</kbd> mid-`rsync`/`mv` can leave files half-copied. Let it
  complete, then verify sizes before deleting the original.
