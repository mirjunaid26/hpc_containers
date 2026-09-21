# Where to Work, and Keeping `$HOME` Under Quota (5 GB)

Your JURECA home directory quota is only **5 GB**. Every `apptainer pull` or
`apptainer build` downloads image layers into `$HOME/.apptainer/cache` by
default — two or three pulls and you can blow through the whole quota,
which then breaks unrelated things (SSH logins, `.bashrc`, everything that
lives in home).

Fix it once, before you pull or build your first image — run this whole
block as-is:

## Quick Fix: Set Up Your Workspace (do this first)

```bash
export WORK=$PROJECT_training2638/container-workshop/$USER
echo "export WORK=$PROJECT_training2638/container-workshop/\$USER" >> ~/.bashrc

mkdir -p $WORK/apptainer_cache $WORK/apptainer_tmp

rm -rf $HOME/.apptainer        # safe if you haven't pulled/built anything yet
ln -s $WORK/apptainer_cache $HOME/.apptainer

export APPTAINER_TMPDIR=$WORK/apptainer_tmp
echo 'export APPTAINER_TMPDIR=$WORK/apptainer_tmp' >> ~/.bashrc
```

Why every line is there:

- **`export WORK=...` + the matching `echo ... >> ~/.bashrc`:** the
  `export` makes `$WORK` usable right now, in this shell; the `echo` line
  makes it survive a new terminal, a reconnect, or coming back tomorrow.
  Without the `echo`, `$WORK` silently goes empty in any *new* shell and
  every command below breaks.
- **`rm -rf $HOME/.apptainer` before the `ln -s`:** if `$HOME/.apptainer`
  already exists as a real directory (e.g. you already ran a `pull` or
  `build` before this), `ln -s` will not replace it — it will silently
  create the link *inside* it instead (`$HOME/.apptainer/apptainer_cache`),
  which does nothing useful. Removing it first guarantees the symlink
  lands where it's supposed to.
- **The symlink** redirects Apptainer's default *cache* location (pulled
  layers, `instances/`, etc.) — it works no matter what actually runs the
  command (interactive shell, job script, `srun`, anything), because it
  redirects the default path itself rather than depending on a variable
  being set.
- **`APPTAINER_TMPDIR`** (+ its own `echo ... >> ~/.bashrc`) covers
  something the symlink doesn't reach: scratch space Apptainer uses
  *while building* an image. There's no fixed default path for this to
  redirect with a symlink — Apptainer falls back to `$TMPDIR`/`/tmp` if
  the variable isn't set — so an environment variable is unavoidable
  here, and it needs the same persistence treatment as `$WORK`.

Two things to remember beyond this block:

1. If you run `apptainer build` from a **Slurm job script**, add the
   `export APPTAINER_TMPDIR=...` line to that script directly too — don't
   rely only on `~/.bashrc` (batch jobs don't always source it).
2. Apptainer does **not** create `apptainer_tmp/` for you. If it's ever
   missing (e.g. you clean project storage later), `build` fails with
   `failed to create build parent dir: stat .../apptainer_tmp: no such
   file or directory` until you `mkdir -p $WORK/apptainer_tmp` again.

Verify it's active:

```bash
ls -ld $HOME/.apptainer
readlink -f $HOME/.apptainer
echo $WORK
echo $APPTAINER_TMPDIR
apptainer cache list
```

## Where to Do Your Exercises & Build Containers

The shared course material lives at `$PROJECT_training2638/container-workshop/`:

```
$PROJECT_training2638/container-workshop/
├── 01_interacting/     <- shared, read-only reference material
├── 02_building/        <- shared, read-only reference material
├── 03_running_on_hpc/  <- shared, read-only reference material
├── ngc_pytorch.sif     <- pre-staged 10 GB NGC image (see tip below)
└── <your-username>/    <- YOUR personal work area ($WORK, set up above)
```

Do all your own work — building images, running exercises, storing
`.sif` files — inside `$WORK`, **not** in `01_interacting/`,
`02_building/`, or `03_running_on_hpc/` (those are shared reference
material for everyone) and **not** in `$HOME` (5 GB quota) or
`/p/scratch` (periodically purged — don't risk losing a container you
just spent time building).

```bash
apptainer build $WORK/my_image.sif my_image.def
```

> **Tip:** for the NGC PyTorch exercises, a `ngc_pytorch.sif` is already
> staged at `$PROJECT_training2638/container-workshop/ngc_pytorch.sif`.
> You don't need to `apptainer pull` your own copy — that image alone is
> 10 GB, twice your entire home quota.

## Check Your Current Usage

```bash
du -shL $HOME/.apptainer   # -L follows the symlink to show the real size
apptainer cache list
```

If `$HOME` is already close to 5 GB, see the next section.

## If You Already Filled Up `$HOME`

If you pulled or built images *before* setting up the symlink above, the
data is sitting in a real `$HOME/.apptainer` directory. Move it across
(don't just delete it — you'd have to re-download/rebuild everything):

```bash
mkdir -p $WORK/apptainer_cache
rsync -av --progress $HOME/.apptainer/ $WORK/apptainer_cache/

# confirm the sizes match before deleting anything
du -sh $HOME/.apptainer
du -sh $WORK/apptainer_cache
```

Only once both sizes match:

```bash
rm -rf $HOME/.apptainer
ln -s $WORK/apptainer_cache $HOME/.apptainer
apptainer cache list   # should report the same totals as before
```

## Common Mistakes to Avoid

- **An `export` without the matching `echo >> ~/.bashrc` doesn't
  survive a new shell.** Both `$WORK` and `$APPTAINER_TMPDIR` need the
  persisted line, not just the one-off `export` — otherwise a new
  terminal, a dropped SSH session, or the next day starts with both
  unset.
- **`ln -s` doesn't replace an existing directory.** If `$HOME/.apptainer`
  already exists as a real directory when you run the symlink command, it
  silently nests the link inside it instead of replacing it. Always
  `rm -rf $HOME/.apptainer` first (safe only because nothing you want to
  keep should be in there yet).
- **`APPTAINER_TMPDIR`'s target must already exist.** Unlike the cache
  symlink, Apptainer will not create `apptainer_tmp/` for you — if it's
  missing, `build` fails until you `mkdir -p $WORK/apptainer_tmp` again.
- **A leftover `~/.bashrc` line can point at a directory that no longer
  exists.** If you changed your setup partway through the workshop, check
  `echo $APPTAINER_TMPDIR` matches a real, existing directory rather than
  assuming an old export is still correct.
- **Environment variables only apply where they're actually set.** A
  Slurm job script needs its own `export` line for `APPTAINER_TMPDIR`,
  not just a reference to your interactive shell's setup.
- **Single quotes block variable expansion.** `export VAR='$WORK/...'`
  writes the literal text `$WORK` into the path instead of its value.
  Always use double quotes or no quotes at all when a `$VAR` is involved.
- **Trailing slashes matter with `rsync`/`mv`.** `source/` copies the
  *contents* of a folder; `source` (no trailing slash) can copy/move the
  whole folder one level deeper than you meant if the destination already
  exists as a directory.
- **Let large transfers finish.** Closing your terminal or hitting
  <kbd>Ctrl-C</kbd> mid-`rsync`/`mv` can leave files half-copied. Let it
  complete, then verify sizes before deleting the original.
