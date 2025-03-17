#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 16:07:34 2024

@author: pedroasvalente
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from BaselineRemoval import BaselineRemoval


# Function to perform baseline correction using BaselineRemoval package
def baseline_correction(spectrum):
    baseObj = BaselineRemoval(spectrum)
    baseline_corrected_spectrum = baseObj.ModPoly(4)  # Adjust polynomial degree as needed
    return baseline_corrected_spectrum

# Step 1: Load the 'CAPILAR' sheet from the Excel file
file_path = '/Users/pedroasvalente/Library/CloudStorage/OneDrive-UniversidadedeCoimbra/02_WORK/05_DATA/001_phd_data_organization/002_5_all_meta.xlsx' # Update the path to your file
geral_data = pd.read_excel(file_path)

# Find the first column that starts with "3050"
start_col = next(col for col in geral_data.columns if str(col).startswith("3050"))
start_col_index = geral_data.columns.get_loc(start_col)
spectral_data = geral_data.iloc[:, start_col_index:].values
wavelengths = geral_data.columns[start_col_index:].astype(float)

print(spectral_data.shape)
print(start_col)
print (wavelengths.shape)
print (wavelengths)

# Apply baseline correction to each spectrum
baseline_corrected_spectral_data = np.apply_along_axis(baseline_correction, axis=1, arr=spectral_data.astype(np.float64))

# Step 3: Normalize the baseline and intensity values using Euclidean normalization
def euclidean_normalization(spectrum):
    euclidean_length = np.linalg.norm(spectrum)
    return spectrum / euclidean_length

# Apply Euclidean normalization to each spectrum
normalized_spectral_data = np.apply_along_axis(euclidean_normalization, axis=1, arr=baseline_corrected_spectral_data)

# Cut intensities between wavenumbers 1850 and 2300
cut_wavelengths_indices = (wavelengths >= 1850) & (wavelengths <= 2500)
normalized_spectral_data[:, cut_wavelengths_indices] = 0

# Create a copy of the original DataFrame with the same structure
updated_capilar_data = geral_data.copy()

# Update the intensity values with the normalized and cut values
updated_capilar_data.iloc[:, start_col_index:] = normalized_spectral_data

# Export the updated DataFrame to a JSON file
output_json_path = '001_1_normalized_spectra.json'
updated_capilar_data.to_json(output_json_path, orient='records', indent=4)

print(f"Updated data has been exported to {output_json_path}")
