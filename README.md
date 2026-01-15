# Robotic Optoacoustic Tomography

This is the official repository for the submission **Robotic Optoacoustic Tomography**.

## Virtual environment setup

To keep dependencies isolated, it is recommended to work inside a Python virtual environment.

On Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

On Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

## Downloading the data

The data required to reproduce the figures is available as assets in the GitHub releases. To download:

1. Navigate to the [Releases](https://github.com/YOUR_USERNAME/YOUR_REPO/releases) page of this repository
2. Download the data archive(s) from the latest release assets
3. Extract the archive(s) to the repository root directory

The extracted data should be organized as follows:

- **Speed analysis data**: `data/speed/Scan_1`, `data/speed/Scan_2`, ..., `data/speed/Scan_8`, each containing an `800_tracking.ts` file and an `800` image folder as used in the paper.
- **Tilting analysis data**: `data/tilting/Scan_1`, `data/tilting/Scan_2`, ..., `data/tilting/Scan_7`, each containing an `800_tracking.ts` file and an `800` image folder.

## Reproducing the figures (speed and tilting analysis)

After installing the dependencies (`pip install -r requirements.txt`) and downloading the data:

You can run the analyses and reproduce the figures/metrics from the repository root with:

```bash
python speed_analysis.py
```

and

```bash
python tilting_analysis.py
```

These commands will:

- Compute PSNR/SSIM metrics and store them as `.csv`, `.xlsx`, and `.png` files in the respective `data/speed` and `data/tilting` folders (see `metrics.py` for details).


