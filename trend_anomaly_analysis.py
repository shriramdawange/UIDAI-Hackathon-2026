"""
UIDAI Hackathon - Trend & Anomaly Detection Analysis
This script analyzes Aadhaar enrolment and demographic update data
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

print("="*60)
print("UIDAI HACKATHON - TREND & ANOMALY DETECTION ANALYSIS")
print("="*60)

# Create output directory if it doesn't exist
import os
output_dir = 'output_visualizations'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"\nCreated output directory: {output_dir}")

# STEP 1: DYNAMIC FILE LOADING
print("\n[STEP 1] Loading CSV files dynamically...")

enrolment_files = []
demographic_files = []

# Walk through the current directory to find CSV files
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.csv'):
            full_path = os.path.join(root, file)
            if 'enrolment' in file.lower():
                enrolment_files.append(full_path)
            elif 'demographic' in file.lower():
                demographic_files.append(full_path)

print(f"\nFound {len(enrolment_files)} enrolment files")
print(f"Found {len(demographic_files)} demographic files")

# Load all enrolment files
print("\nLoading enrolment data...")
df_enrolment_list = []
for file in enrolment_files:
    print(f"  - Loading: {file}")
    df_temp = pd.read_csv(file)
    df_enrolment_list.append(df_temp)

df_enrolment = pd.concat(df_enrolment_list, ignore_index=True)
print(f"Total enrolment records: {len(df_enrolment):,}")

# Load all demographic files
print("\nLoading demographic update data...")
df_update_list = []
for file in demographic_files:
    print(f"  - Loading: {file}")
    df_temp = pd.read_csv(file)
    df_update_list.append(df_temp)

df_update = pd.concat(df_update_list, ignore_index=True)
print(f"Total demographic update records: {len(df_update):,}")

# Display first 5 rows and columns
print("\n" + "="*60)
print("ENROLMENT DATA - First 5 Rows:")
print("="*60)
print(df_enrolment.head())
print(f"\nColumns: {list(df_enrolment.columns)}")

print("\n" + "="*60)
print("DEMOGRAPHIC UPDATE DATA - First 5 Rows:")
print("="*60)
print(df_update.head())
print(f"\nColumns: {list(df_update.columns)}")

# STEP 2: DATA CLEANING
print("\n[STEP 2] Cleaning data...")

# Convert date columns to datetime
if 'date' in df_enrolment.columns:
    df_enrolment['date'] = pd.to_datetime(df_enrolment['date'], format='%d-%m-%Y', errors='coerce')
if 'date' in df_update.columns:
    df_update['date'] = pd.to_datetime(df_update['date'], format='%d-%m-%Y', errors='coerce')

# Handle missing values
print(f"\nEnrolment missing values before cleaning:\n{df_enrolment.isnull().sum()}")
print(f"\nUpdate missing values before cleaning:\n{df_update.isnull().sum()}")

# Drop rows with missing critical data (state)
df_enrolment = df_enrolment.dropna(subset=['state'])
df_update = df_update.dropna(subset=['state'])

print(f"\nAfter cleaning:")
print(f"  Enrolment records: {len(df_enrolment):,}")
print(f"  Update records: {len(df_update):,}")

# STEP 3: ANALYSIS & VISUALIZATION
print("\n[STEP 3] Performing analysis and creating visualizations...")

# 1. TREND ANALYSIS - Enrolments by Age Group
print("\n1. Creating Trend Analysis (Enrolments by Age Group)...")

# Identify age group columns
age_columns = [col for col in df_enrolment.columns if 'age' in col.lower()]
print(f"   Age columns found: {age_columns}")

# Create age group analysis
age_data = {}
for col in age_columns:
    age_data[col] = df_enrolment[col].sum()

# Create DataFrame for plotting
age_df = pd.DataFrame(list(age_data.items()), columns=['Age Group', 'Total Enrolments'])
age_df = age_df.sort_values('Total Enrolments', ascending=False)

# Create bar chart
plt.figure(figsize=(12, 6))
bars = plt.bar(range(len(age_df)), age_df['Total Enrolments'], color='steelblue', edgecolor='black')
plt.xlabel('Age Group', fontsize=12, fontweight='bold')
plt.ylabel('Total Enrolments', fontsize=12, fontweight='bold')
plt.title('Trend Analysis: Total Enrolments by Age Group', fontsize=14, fontweight='bold', pad=20)
plt.xticks(range(len(age_df)), age_df['Age Group'], rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)

# Add value labels on bars
for i, bar in enumerate(bars):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height):,}',
             ha='center', va='bottom', fontsize=9)

plt.tight_layout()
output_path = os.path.join(output_dir, 'trend_analysis.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"   ✓ Saved: {output_path}")
plt.close()

# 2. ANOMALY DETECTION - State-wise Update to Enrolment Ratio
print("\n2. Creating Anomaly Detection (State-wise Ratio)...")

# Aggregate enrolment by state
enrolment_by_state = df_enrolment.groupby('state')[age_columns].sum().sum(axis=1).reset_index()
enrolment_by_state.columns = ['state', 'total_enrolment']

# Aggregate updates by state
update_age_columns = [col for col in df_update.columns if 'age' in col.lower() or 'demo' in col.lower()]
if not update_age_columns:
    # If no age columns, count rows
    update_by_state = df_update.groupby('state').size().reset_index()
    update_by_state.columns = ['state', 'total_update']
else:
    update_by_state = df_update.groupby('state')[update_age_columns].sum().sum(axis=1).reset_index()
    update_by_state.columns = ['state', 'total_update']

# Merge datasets
merged_df = pd.merge(enrolment_by_state, update_by_state, on='state', how='inner')

# Calculate ratio
merged_df['Update_to_Enrolment_Ratio'] = merged_df['total_update'] / merged_df['total_enrolment']

# Sort and get top 10 anomalies
top_10_anomalies = merged_df.nlargest(10, 'Update_to_Enrolment_Ratio')

print(f"\n   Top 10 States with Highest Update-to-Enrolment Ratios:")
print(top_10_anomalies[['state', 'Update_to_Enrolment_Ratio']].to_string(index=False))

# Create horizontal bar chart
plt.figure(figsize=(12, 8))
bars = plt.barh(range(len(top_10_anomalies)), top_10_anomalies['Update_to_Enrolment_Ratio'], 
                color='coral', edgecolor='black')
plt.yticks(range(len(top_10_anomalies)), top_10_anomalies['state'])
plt.xlabel('Update-to-Enrolment Ratio', fontsize=12, fontweight='bold')
plt.ylabel('State', fontsize=12, fontweight='bold')
plt.title('Anomaly Detection: Top 10 States with Highest Update-to-Enrolment Ratios', 
          fontsize=14, fontweight='bold', pad=20)
plt.grid(axis='x', alpha=0.3)

# Add value labels on bars
for i, bar in enumerate(bars):
    width = bar.get_width()
    plt.text(width, bar.get_y() + bar.get_height()/2.,
             f'{width:.3f}',
             ha='left', va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
output_path = os.path.join(output_dir, 'anomaly_detection.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"   ✓ Saved: {output_path}")
plt.close()

# STEP 4: SUMMARY
print("\n" + "="*60)
print("ANALYSIS COMPLETE!")
print("="*60)
print("\nOutput files created:")
print(f"  1. {os.path.join(output_dir, 'trend_analysis.png')} - Bar chart of enrolments by age group")
print(f"  2. {os.path.join(output_dir, 'anomaly_detection.png')} - Top 10 states with highest update ratios")
print("\nKey Insights:")
print(f"  - Total enrolment records analyzed: {len(df_enrolment):,}")
print(f"  - Total update records analyzed: {len(df_update):,}")
print(f"  - Number of states analyzed: {len(merged_df)}")
print(f"  - Highest anomaly ratio: {top_10_anomalies.iloc[0]['Update_to_Enrolment_Ratio']:.3f} ({top_10_anomalies.iloc[0]['state']})")
print("\n" + "="*60)
