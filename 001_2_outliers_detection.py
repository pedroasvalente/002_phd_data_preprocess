import json
import pandas as pd
import numpy as np
import scipy.stats as stats
from scipy.spatial.distance import mahalanobis

# Step 1: Load JSON Data
json_file = "001_1_normalized_spectra.json"  # Update this with your actual JSON file path
with open(json_file, "r") as file:
    data = json.load(file)

# Step 2: Convert JSON into a DataFrame
df_list = []
for sample in data:
    sample_id = sample["id"]
    sample_type = sample["sample_type"]
    group = sample["group"]
    timepoint = sample["timepoint"]

    # Extract wavenumbers and intensities
    wavenumbers = sample["wavenumbers"]
    intensities = sample["intensities"]

    # Create DataFrame for each sample
    df_sample = pd.DataFrame({
        "ID": sample_id,
        "Sample_Type": sample_type,
        "Group": group,
        "Timepoint": timepoint,
        "Wavenumber": wavenumbers,
        "Intensity": intensities
    })
    df_list.append(df_sample)

# Combine all samples into a single DataFrame
df = pd.concat(df_list, ignore_index=True)

# Step 3: Apply Z-score Outlier Detection Per Sample Type
cleaned_dfs = []

for sample_type, df_sample in df.groupby("Sample_Type"):
    print(f"Processing Sample Type: {sample_type}")

    # Apply Z-score method
    z_scores = np.abs(stats.zscore(df_sample["Intensity"]))
    df_zscore = df_sample[z_scores < 3]

    # Save cleaned dataset for this sample type
    df_zscore.to_csv(f"cleaned_FTIR_Zscore_{sample_type}.csv", index=False)
    cleaned_dfs.append(df_zscore)

# Step 4: Merge All Cleaned Data (if needed)
df_cleaned_all = pd.concat(cleaned_dfs, ignore_index=True)
df_cleaned_all.to_csv("cleaned_FTIR_ALL.csv", index=False)

print("✅ Z-score outlier detection completed for each sample type! Cleaned files saved.")
