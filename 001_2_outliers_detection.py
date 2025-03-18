import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import os

# Step 1: Load Excel Data
file_path = "001_1_normalized_spectra.xlsx"
geral_data = pd.read_excel(file_path)

# Identify metadata and spectral data
start_col = next(col for col in geral_data.columns if str(col).startswith("3050"))
start_col_index = geral_data.columns.get_loc(start_col)

metadata = geral_data.iloc[:, :start_col_index]  # Metadata columns
spectral_data = geral_data.iloc[:, start_col_index:]  # Spectral columns (intensities)

# Step 2: Set up output directories
# Create necessary directories
output_dir = "001_3_output_outliers_detection"
plot_dir_kept = os.path.join(output_dir, "plots", "kept")
plot_dir_deleted = os.path.join(output_dir, "plots", "deleted")
os.makedirs(output_dir, exist_ok=True)
os.makedirs(plot_dir_kept, exist_ok=True)
os.makedirs(plot_dir_deleted, exist_ok=True)

# Step 3: Apply Z-score Outlier Detection per Sample Type
cleaned_dfs = []
deleted_dfs = []
outlier_counts = {}

for sample_type, group_data in geral_data.groupby("sample_type"):

    # Separate metadata and spectral data
    group_metadata = group_data.iloc[:, :start_col_index]
    group_spectral_data = group_data.iloc[:, start_col_index:]

    # Compute Z-score for entire spectra
    z_scores = np.abs(stats.zscore(group_spectral_data, nan_policy='omit'))
    outlier_mask = np.any(z_scores >= 5, axis=1)
    outlier_count = np.sum(outlier_mask)

    # Store outlier count per sample type
    outlier_counts[sample_type] = int(outlier_count)

    # Keep only non-outlier spectra
    cleaned_group_data = group_data[~outlier_mask]
    cleaned_dfs.append(cleaned_group_data)

    # Store removed (outlier) spectra
    deleted_group_data = group_data[outlier_mask]
    deleted_dfs.append(deleted_group_data)

    # Step 4: Save Plots - Kept Spectra
    plt.figure(figsize=(10, 6))
    for i in range(cleaned_group_data.shape[0]):
        plt.plot(cleaned_group_data.columns[start_col_index:].astype(float),
                 cleaned_group_data.iloc[i, start_col_index:].values, alpha=0.5)
    plt.xlabel("Wavenumber")
    plt.ylabel("Intensity")
    plt.title(f"Kept Spectra - {sample_type}")
    plt.grid(True)
    kept_plot_path = os.path.join(plot_dir_kept, f"03_kept_spectra_{sample_type}.png")
    plt.savefig(kept_plot_path, dpi=300)
    plt.close()

    # Step 5: Save Plots - Deleted Spectra
    if not deleted_group_data.empty:
        plt.figure(figsize=(10, 6))
        for i in range(deleted_group_data.shape[0]):
            plt.plot(deleted_group_data.columns[start_col_index:].astype(float),
                     deleted_group_data.iloc[i, start_col_index:].values, alpha=0.5, color="red")
        plt.xlabel("Wavenumber")
        plt.ylabel("Intensity")
        plt.title(f"Deleted Spectra - {sample_type}")
        plt.grid(True)
        deleted_plot_path = os.path.join(plot_dir_deleted, f"deleted_spectra_{sample_type}.png")
        plt.savefig(deleted_plot_path, dpi=300)
        plt.close()

# Merge all cleaned and deleted data
cleaned_data = pd.concat(cleaned_dfs, ignore_index=True)
deleted_data = pd.concat(deleted_dfs, ignore_index=True)

# Step 6: Export CSV files
# Save the main cleaned dataset **outside** the output folder (for direct pipeline use)
cleaned_data.to_csv("001_3_cleaned_FTIR.csv", index=False)

# Save cleaned data per sample type in the output folder
for sample_type, group_data in cleaned_data.groupby("sample_type"):
    group_data.to_csv(os.path.join(output_dir, f"02_cleaned_FTIR_´{sample_type}.csv"), index=False)

# Save all deleted spectra in the output folder
deleted_data.to_csv(os.path.join(output_dir, "01_deleted_FTIR.csv"), index=False)

# Print outlier summary
print("Outlier counts per sample type:")
for sample_type, count in outlier_counts.items():
    print(f"   - {sample_type}: {count} entire spectra removed as outliers")
