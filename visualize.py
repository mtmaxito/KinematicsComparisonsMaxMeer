import pandas as pd
import matplotlib.pyplot as plt
import os
from glob import glob


def plot_stacked_variables(csv_path, out_path):
    df = pd.read_csv(csv_path)
    frame_cols = [col for col in df.columns if col.lower() == 'frame']
    if not frame_cols:
        frame_cols = [col for col in df.columns if 'frame' in col.lower()]
    frame_col = frame_cols[0]
    y_cols = [col for col in df.columns if 'frame' not in col.lower() and 'true frame' not in col.lower() and pd.api.types.is_numeric_dtype(df[col])]
    n = len(y_cols)
    fig, axes = plt.subplots(n, 1, figsize=(10, 2*n), sharex=True)
    if n == 1:
        axes = [axes]
    for i, col in enumerate(y_cols):
        axes[i].plot(df[frame_col], df[col])
        axes[i].set_ylabel(col)
        axes[i].grid(True)
    axes[-1].set_xlabel(frame_col)
    fig.suptitle(f"Stacked plots: {os.path.basename(csv_path)}")
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path)
    plt.close(fig)
    print(f"Saved {out_path}")


def plot_overlay_matching_columns(raven_csv, trakstar_csv, out_dir):
    df_raven = pd.read_csv(raven_csv)
    df_trakstar = pd.read_csv(trakstar_csv)
    frame_col_raven = next((col for col in df_raven.columns if col.lower() == 'frame'), None)
    if not frame_col_raven:
        frame_col_raven = next((col for col in df_raven.columns if 'frame' in col.lower()), None)
    frame_col_trakstar = next((col for col in df_trakstar.columns if col.lower() == 'frame'), None)
    if not frame_col_trakstar:
        frame_col_trakstar = next((col for col in df_trakstar.columns if 'frame' in col.lower()), None)
    raven_cols = set(df_raven.columns) - {frame_col_raven}
    trakstar_cols = set(df_trakstar.columns) - {frame_col_trakstar}
    matching_cols = [col for col in raven_cols & trakstar_cols if pd.api.types.is_numeric_dtype(df_raven[col]) and pd.api.types.is_numeric_dtype(df_trakstar[col])]
    if not matching_cols:
        print("No matching columns found for overlay.")
        return
    os.makedirs(out_dir, exist_ok=True)
    for col in matching_cols:
        x_raven = df_raven[frame_col_raven] - df_raven[frame_col_raven].iloc[0] + 18
        y_raven = df_raven[col]
        x_trakstar = df_trakstar[frame_col_trakstar] - df_trakstar[frame_col_trakstar].iloc[0]
        y_trakstar = df_trakstar[col]
        plt.figure(figsize=(10, 4))
        plt.plot(x_raven, y_raven, label='Raven', color='blue')
        plt.plot(x_trakstar, y_trakstar, label='TrakStar', color='orange', alpha=0.7)
        plt.title(f"Overlay: {col}")
        plt.xlabel('Frame (aligned start)')
        plt.ylabel(col)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        out_path = os.path.join(out_dir, f'overlay_{col}.png')
        plt.savefig(out_path)
        plt.close()
        print(f"Saved overlay plot: {out_path}")


def process_trial(csv_path, trial_plot_dir, trial_path=None):
    stacked_out_path = os.path.join(trial_plot_dir, 'stacked.png')
    plot_stacked_variables(csv_path, stacked_out_path)
    if trial_path and os.path.isdir(trial_path):
        raven_file = None
        trakstar_file = None
        for fname in os.listdir(trial_path):
            if fname.endswith('.csv') and 'frames' not in fname.lower():
                if 'trakstar_final' in fname.lower():
                    trakstar_file = os.path.join(trial_path, fname)
                elif 'trakstar' not in fname.lower():
                    raven_file = os.path.join(trial_path, fname)
        if raven_file and trakstar_file:
            overlay_dir = os.path.join(trial_plot_dir, 'overlays')
            plot_overlay_matching_columns(raven_file, trakstar_file, overlay_dir)


def plot_all_trials(processed_dir, out_dir, dataset_dir):
    for csv_path in glob(os.path.join(processed_dir, '*.csv')):
        trial_name = os.path.splitext(os.path.basename(csv_path))[0]
        if trial_name.lower().startswith('aligned_'):
            trial_folder = trial_name[len('aligned_'):]
            trial_path = os.path.join(dataset_dir, trial_folder)
            trial_plot_dir = os.path.join(out_dir, trial_folder)
            process_trial(csv_path, trial_plot_dir, trial_path)


if __name__ == "__main__":
    plot_all_trials(processed_dir='processed_csvs', out_dir='plots', dataset_dir='dataset/January 2023')
