README: FTIR Spectral Data Processing Pipeline
------
Overview
This folder contains the scripts and data files for processing FTIR spectral data, including baseline correction, normalization, outlier detection, and dataset analysis. The pipeline ensures data quality and prepares it for further scientific analysis.
-------
Folder Contents
1️⃣ Scripts (Processing Steps)
Filename	Description
001_0_baseline_correction_normalization.py	Performs baseline correction and normalization on raw spectral data.
001_2_outliers_detection.py	Identifies and removes outlier spectra using the Z-score method.
001_4_df_metrics.py	Analyzes the cleaned dataset, summarizing sample counts by type, category, and timepoint.
------
2️⃣ Data Files
Filename	Description
001_1_normalized_spectra.xlsx	Normalized spectral data after baseline correction.
001_3_cleaned_FTIR.csv	Cleaned dataset after outlier detection (main dataset for further analysis).
001_5_metrics.json	JSON file summarizing sample counts by type, category, and timepoint.
------------##--------------
Pipeline Workflow
------------##--------------

--

1️⃣ Baseline Correction & Normalization
Run 001_0_baseline_correction_normalization.py to process raw FTIR data.
Output: 001_1_normalized_spectra.xlsx

--

2️⃣ Outlier Detection
Run 001_2_outliers_detection.py to remove outlier spectra.
Output: 001_3_cleaned_FTIR.csv

--

3️⃣ Dataset Analysis
Run 001_4_df_metrics.py to analyze the cleaned dataset.
Output: 001_5_metrics.json (summary statistics).
How to Use
Run the scripts in sequence (001_0 → 001_2 → 001_4).
Use 001_3_cleaned_FTIR.csv as the final cleaned dataset.
Check 001_5_metrics.json for sample distribution details.