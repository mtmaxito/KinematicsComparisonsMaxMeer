# Multimoal Data Collection System for Robot-Assisted Surgery

## Task: Comparison of Kinematics from Raven Surgical Robot and TrakStar Motion Tracking System

### Objective
The goal of this project is to provide an understanding of different data modalities and how to manipulate, visualize, and analyze them effectively in the context of a robotic surgery project.

---

## Folder Structure
- `process_csvs.py` — Loads and robustly aligns Raven and TrakStar CSVs for each trial
- `visualize.py` — Generates stacked plots for all variables in each dataset
- `processed_csvs/` — Output directory for aligned CSVs
- `plots/` — Output directory for generated figures
- `dataset/January 2023` — Raw data (can be replaced if same naming schemes are followed)

---

## Setup
1. Install dependencies:
   ```bash
   pip install pandas matplotlib
   ```
2. Place dataset in the `dataset/January 2023/` directory as described above.

---

## Usage

### 1. Data Loading & Alignment
Run the following to process and align the Raven and TrakStar CSVs for each trial:
```bash
python process_csvs.py
```
- **Input:**
  - Raven Kinematic File: `Peg_Transfer_S01_T{trial}.csv`
  - TrakStar Kinematic File: `Peg_Transfer_S01_T{trial}_trakStar_final.csv`
- **Output:** Aligned CSVs saved in `processed_csvs/`.

### 2. Data Visualization
#### A. Stacked Plots (Individual Datasets)
Generate stacked plots for each relevant variable in both datasets:
```bash
python visualize.py
```
- Two figures will be generated for each trial:
  - One with subplots for all Raven variables
  - One with subplots for all TrakStar variables
- Plots are saved in `plots/`.

#### B. Visual Variable Comparison
- The stacked plots can be visually compared to hypothesize which variables from Raven and TrakStar correspond to each other.
- The pairs identified between the Raven and TrakStar files are present in the overlaid plots explained next.

#### C. Alignment via Manipulation
- Variable pairs sharing the same name between the Raven and TrakStar files were used per trial.
- Raven variables were shifted by 18 frames to the right due to them not containing frames for 0-17.
- Visualized the transformed TrakStar variable overlaid with the Raven variable to assess alignment and are saved in `plots/Peg_Transfer_SKay_T{trial number}_27-01-2023_16-27-20/overlays/`.

