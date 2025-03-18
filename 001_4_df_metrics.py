import pandas as pd
import json

# Load the cleaned dataset
file_path = '001_3_cleaned_FTIR.csv'
cleaned_data = pd.read_csv(file_path)

# Standardize column values (without changing case for sample_type)
cleaned_data['sample_type'] = cleaned_data['sample_type'].str.strip()
cleaned_data['group_fam'] = cleaned_data['group_fam'].str.strip().str.lower()
cleaned_data['timepoint'] = cleaned_data['timepoint'].str.strip().str.upper()

# Define sample types and categories
sample_types = ['SERUM', 'PLASMA', 'CAPILAR', 'URINE', 'SALIVA']
categories = ['football', 'ultrarunning', 'sedentary']

def count_samples(df, sample_type):
    """Counts the total samples and breakdown by category and time point."""
    sample_df = df[df['sample_type'] == sample_type]  # Matches exact uppercase values
    total_samples = len(sample_df)

    category_counts = {}
    for category in categories:
        category_df = sample_df[sample_df['group_fam'] == category]
        category_counts[category] = {
            'Total': len(category_df),
            'T1': len(category_df[category_df['timepoint'] == 'T1']),
            'T2': len(category_df[category_df['timepoint'] == 'T2']),
            'T3': len(category_df[category_df['timepoint'] == 'T3']) if 'T3' in df['timepoint'].unique() else 0
        }

    return total_samples, category_counts

# Run the analysis
results = {}
for sample in sample_types:
    total, breakdown = count_samples(cleaned_data, sample)
    results[sample] = {'Total Samples': total, 'Breakdown': breakdown}

# Export results to JSON
output_file = "001_5_metrics.json"
with open(output_file, 'w') as f:
    json.dump(results, f, indent=4)

# Print results
print(json.dumps(results, indent=4))
