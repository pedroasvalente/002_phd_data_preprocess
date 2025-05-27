FTIR Spectral Preprocessing Pipeline

This repository provides the complete preprocessing pipeline for Fourier Transform Infrared (FTIR) spectra derived from multiple human biofluids, collected across distinct physical activity profiles. It was developed to support a scientific study aiming to explore biochemical signatures of exercise using infrared spectroscopy.

🧪 Scientific Context

The project investigates whether FTIR spectroscopy can differentiate individuals based on physical activity levels — including football players, ultramarathon runners, and sedentary individuals — using spectral data from biofluids such as serum, plasma, capillary blood, saliva, and urine. This repository contains the reproducible code and intermediate data products referenced in the associated manuscript.

📂 Repository Contents
.
├── 000_all_meta.xlsx                  # Raw metadata: participant IDs, sample types, group classifications
├── 001_0_baseline_correction_normalization.py  # Script for baseline correction and vector normalization
├── 001_1_normalized_spectra.xlsx      # Output of normalized spectra
├── 001_2_outliers_detection.py        # PCA-based outlier detection and removal
├── 001_3_cleaned_FTIR.csv             # Final cleaned dataset for statistical and ML analyses
├── 001_4_df_metrics.py                # Script to compute group/sample metrics
├── 001_5_metrics.json                 # Summary statistics per group and biofluid
├── README.md                          # This documentation file

🧬 Data Summary
	•	Total samples: Multiple hundreds across five biofluids
	•	Sample classes: Football, ultrarunning, sedentary
	•	Timepoints: Baseline and post-intervention (if applicable)
	•	Target variables: Group classification, timepoint, VO2max class, body fat class

🔬 Preprocessing Pipeline

1. Baseline Correction & Normalization
	•	Spectra undergo baseline correction to remove background absorption.
	•	Vector normalization standardizes intensity variation between samples.

2. Outlier Detection
	•	Principal Component Analysis (PCA) is used to identify spectral outliers.
	•	Outliers are excluded from downstream analyses to improve data robustness.

3. Metadata Integration
	•	Metadata from 000_all_meta.xlsx is merged with cleaned spectral data.
	•	Final dataset (001_3_cleaned_FTIR.csv) is structured for supervised learning.

4. Summary Metrics
	•	The script 001_4_df_metrics.py compiles sample distributions and class frequencies.
	•	Results are saved to 001_5_metrics.json, used to validate sample balance across conditions.

📊 Applications

The resulting cleaned dataset is suitable for:
	•	Supervised classification (e.g., group, fitness class prediction)
	•	Exploratory spectral analysis
	•	Dimensionality reduction (e.g., PLS-DA, PCA)
	•	Biomarker discovery in exercise physiology

Important: This repository is not intended for public reuse or active development. It accompanies the manuscript entitled ”FTIR-Based Digital Fingerprint Enables Discrimination Between Sedentary Individuals and Ultrarunning and Football Athletes via Supervised Machine Learning – the development of a biochemical digital fingerprint” as supplementary material.
