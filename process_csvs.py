import pandas as pd
import os

def align_by_timestamp(df1, df2, time_col1, time_col2):
    df1 = df1.copy()
    df2 = df2.copy()
    df1 = df1.dropna(subset=[time_col1])
    df2 = df2.dropna(subset=[time_col2])
    df1 = df1.sort_values(time_col1)
    df2 = df2.sort_values(time_col2)
    aligned = pd.merge_asof(
        df1,
        df2,
        left_on=time_col1,
        right_on=time_col2,
        direction='forward',
        suffixes=('_raven', '_trakstar')
    )
    return aligned

def find_trial_csvs(trial_path):
    raven_file = None
    trakstar_file = None
    for fname in os.listdir(trial_path):
        if fname.endswith('.csv') and 'frames' not in fname.lower():
            if 'trakstar_final' in fname.lower():
                trakstar_file = os.path.join(trial_path, fname)
            elif 'trakstar' not in fname.lower():
                raven_file = os.path.join(trial_path, fname)
    return raven_file, trakstar_file

def extract_time_column(df):
    cols = [col for col in df.columns if 'True frame #' in col]
    return cols[0] if cols else None

def process_single_trial(trial_path, out_dir):
    raven_file, trakstar_file = find_trial_csvs(trial_path)
    if not (raven_file and trakstar_file):
        return False
    df_raven = pd.read_csv(raven_file)
    df_trakstar = pd.read_csv(trakstar_file)
    time_col_raven = extract_time_column(df_raven)
    time_col_trakstar = extract_time_column(df_trakstar)
    if not (time_col_raven and time_col_trakstar):
        return False
    aligned = align_by_timestamp(
        df_raven, df_trakstar, time_col_raven, time_col_trakstar
    )
    trial_folder = os.path.basename(trial_path)
    out_file = os.path.join(out_dir, f'aligned_{trial_folder}.csv')
    aligned.to_csv(out_file, index=False)
    print(f"Processed and aligned: {trial_folder}")
    return True

def process_all_trials(dataset_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for trial_folder in os.listdir(dataset_dir):
        trial_path = os.path.join(dataset_dir, trial_folder)
        if not os.path.isdir(trial_path):
            continue
        process_single_trial(trial_path, out_dir)

if __name__ == "__main__":
    process_all_trials(dataset_dir='dataset/January 2023', out_dir='processed_csvs')