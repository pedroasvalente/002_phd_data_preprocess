import pandas as pd
import numpy as np
from BaselineRemoval import BaselineRemoval

# Function to perform baseline correction using BaselineRemoval package
def baseline_correction(spectrum):
    baseObj = BaselineRemoval(spectrum)
    return baseObj.ModPoly(4)  # Adjust polynomial degree as needed

# Function to perform Euclidean normalization
def euclidean_normalization(spectrum):
    euclidean_length = np.linalg.norm(spectrum)
    return spectrum / euclidean_length if euclidean_length != 0 else spectrum

# Step 1: Load the Excel file
file_path = '000_all_meta.xlsx'  # Update the path to your file
geral_data = pd.read_excel(file_path)

# Find the first column that starts with "3050"
start_col = next(col for col in geral_data.columns if str(col).startswith("3050"))
start_col_index = geral_data.columns.get_loc(start_col)

# Extract spectral data and wavelengths
spectral_data = geral_data.iloc[:, start_col_index:].values.astype(np.float64)
wavelengths = geral_data.columns[start_col_index:].astype(float)

# Apply baseline correction to each spectrum
baseline_corrected_spectral_data = np.apply_along_axis(baseline_correction, axis=1, arr=spectral_data)

# Apply Euclidean normalization
normalized_spectral_data = np.apply_along_axis(euclidean_normalization, axis=1, arr=baseline_corrected_spectral_data)

# Identify columns to keep (excluding the cut range 1850-2500)
valid_wavelengths_mask = (wavelengths < 1850) | (wavelengths > 2500)
wavelengths_filtered = wavelengths[valid_wavelengths_mask]
normalized_spectral_data_filtered = normalized_spectral_data[:, valid_wavelengths_mask]

# Create a new DataFrame with the same structure but excluding the cut range
output_data = geral_data.iloc[:, :start_col_index].copy()
output_data = pd.concat([output_data, pd.DataFrame(normalized_spectral_data_filtered, columns=wavelengths_filtered)], axis=1)

# Save the modified data to a new Excel file
output_excel_path = '001_1_normalized_spectra.xlsx'
output_data.to_excel(output_excel_path, index=False)