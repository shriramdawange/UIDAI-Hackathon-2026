"""
UIDAI Hackathon - Advanced Anomaly Detection
Professional Publication-Quality Visualizations
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Set professional theme
sns.set_theme(style="whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9

print("="*70)
print("UIDAI HACKATHON - ADVANCED ANOMALY DETECTION")
print("Professional Publication-Quality Visualizations")
print("="*70)

# Create output directory if it doesn't exist
output_dir = 'output_visualizations'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"\nCreated output directory: {output_dir}")

# STEP 1: SETUP & DATA LOADING
print("\n[STEP 1] Loading and preparing data...")

enrolment_files = []
demographic_files = []

# Find CSV files dynamically
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.csv'):
            full_path = os.path.join(root, file)
            if 'enrolment' in file.lower():
                enrolment_files.append(full_path)
            elif 'demographic' in file.lower():
                demographic_files.append(full_path)

print(f"Found {len(enrolment_files)} enrolment files")
print(f"Found {len(demographic_files)} demographic files")

# Load enrolment data
print("\nLoading enrolment data...")
df_enrolment_list = []
for file in enrolment_files:
    df_temp = pd.read_csv(file)
    df_enrolment_list.append(df_temp)
df_enrolment = pd.concat(df_enrolment_list, ignore_index=True)

# Load demographic update data
print("Loading demographic update data...")
df_update_list = []
for file in demographic_files:
    df_temp = pd.read_csv(file)
    df_update_list.append(df_temp)
df_update = pd.concat(df_update_list, ignore_index=True)

print(f"\nTotal enrolment records: {len(df_enrolment):,}")
print(f"Total update records: {len(df_update):,}")

# Data aggregation
print("\nAggregating data by state...")

# Get age columns
enrolment_age_cols = [col for col in df_enrolment.columns if 'age' in col.lower()]
update_age_cols = [col for col in df_update.columns if 'age' in col.lower() or 'demo' in col.lower()]

# Aggregate enrolments by state
enrolment_by_state = df_enrolment.groupby('state')[enrolment_age_cols].sum().sum(axis=1).reset_index()
enrolment_by_state.columns = ['state', 'Enrolment_Count']

# Aggregate updates by state
if update_age_cols:
    update_by_state = df_update.groupby('state')[update_age_cols].sum().sum(axis=1).reset_index()
else:
    update_by_state = df_update.groupby('state').size().reset_index()
update_by_state.columns = ['state', 'Update_Count']

# Merge datasets
merged_df = pd.merge(enrolment_by_state, update_by_state, on='state', how='inner')

# Calculate Update Ratio
merged_df['Update_Ratio'] = merged_df['Update_Count'] / merged_df['Enrolment_Count']

# Sort by ratio
merged_df = merged_df.sort_values('Update_Ratio', ascending=False).reset_index(drop=True)

print(f"States analyzed: {len(merged_df)}")
print(f"\nUpdate Ratio Statistics:")
print(f"  Mean: {merged_df['Update_Ratio'].mean():.2f}")
print(f"  Median: {merged_df['Update_Ratio'].median():.2f}")
print(f"  Std Dev: {merged_df['Update_Ratio'].std():.2f}")
print(f"  Min: {merged_df['Update_Ratio'].min():.2f}")
print(f"  Max: {merged_df['Update_Ratio'].max():.2f}")

# STEP 2: GENERATE ADVANCED VISUALIZATIONS
print("\n[STEP 2] Creating advanced visualizations...")

# ============================================================================
# VISUALIZATION 1: STATISTICAL OUTLIER DETECTION (Box Plot)
# ============================================================================
print("\n1. Creating Statistical Outlier Detection (Box Plot)...")

fig, ax = plt.subplots(figsize=(12, 8))

# Create box plot
box_parts = ax.boxplot([merged_df['Update_Ratio']], 
                        vert=True, 
                        patch_artist=True,
                        widths=0.5,
                        showmeans=True,
                        meanprops=dict(marker='D', markerfacecolor='red', markersize=8, label='Mean'))

# Style the box
box_parts['boxes'][0].set_facecolor('lightblue')
box_parts['boxes'][0].set_edgecolor('darkblue')
box_parts['boxes'][0].set_linewidth(2)

# Style whiskers and caps
for whisker in box_parts['whiskers']:
    whisker.set(color='darkblue', linewidth=1.5, linestyle='--')
for cap in box_parts['caps']:
    cap.set(color='darkblue', linewidth=2)

# Style median line
box_parts['medians'][0].set(color='darkgreen', linewidth=2.5)

# Style outliers
box_parts['fliers'][0].set(marker='o', markerfacecolor='red', markersize=8, 
                           markeredgecolor='darkred', alpha=0.7)

# Calculate outliers using IQR method
Q1 = merged_df['Update_Ratio'].quantile(0.25)
Q3 = merged_df['Update_Ratio'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = merged_df[merged_df['Update_Ratio'] > upper_bound]
print(f"   Statistical outliers detected: {len(outliers)}")

# Add annotations for top outliers
for idx, row in outliers.head(5).iterrows():
    ax.annotate(f"{row['state']}\n({row['Update_Ratio']:.1f})", 
                xy=(1, row['Update_Ratio']),
                xytext=(1.3, row['Update_Ratio']),
                fontsize=8,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', color='red'))

# Add statistical reference lines
ax.axhline(y=merged_df['Update_Ratio'].mean(), color='red', linestyle='--', 
           linewidth=1.5, alpha=0.7, label=f'Mean: {merged_df["Update_Ratio"].mean():.2f}')
ax.axhline(y=merged_df['Update_Ratio'].median(), color='green', linestyle='--', 
           linewidth=1.5, alpha=0.7, label=f'Median: {merged_df["Update_Ratio"].median():.2f}')
ax.axhline(y=upper_bound, color='orange', linestyle=':', 
           linewidth=2, alpha=0.8, label=f'Outlier Threshold: {upper_bound:.2f}')

ax.set_ylabel('Update-to-Enrolment Ratio', fontweight='bold', fontsize=12)
ax.set_title('Statistical Outliers in Demographic Updates\nBox Plot Analysis with IQR Method', 
             fontweight='bold', fontsize=14, pad=20)
ax.set_xticks([1])
ax.set_xticklabels(['All States'], fontsize=11)
ax.legend(loc='upper right', framealpha=0.9)
ax.grid(True, alpha=0.3, axis='y')

# Add text box with statistics
stats_text = f'Total States: {len(merged_df)}\nOutliers: {len(outliers)}\nIQR: {IQR:.2f}\nQ1: {Q1:.2f}\nQ3: {Q3:.2f}'
ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=9,
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
output_path = os.path.join(output_dir, 'advanced_boxplot_outliers.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"   ✓ Saved: {output_path}")
plt.close()

# ============================================================================
# VISUALIZATION 2: INTENSITY HEATMAP (Top 20 States)
# ============================================================================
print("\n2. Creating State-wise Risk Heatmap...")

# Get top 20 states by total activity (enrolment + update)
merged_df['Total_Activity'] = merged_df['Enrolment_Count'] + merged_df['Update_Count']
top_20_states = merged_df.nlargest(20, 'Total_Activity').copy()

# Normalize the data for heatmap (0-1 scale)
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

heatmap_data = top_20_states[['Enrolment_Count', 'Update_Count', 'Update_Ratio']].copy()
heatmap_data_normalized = pd.DataFrame(
    scaler.fit_transform(heatmap_data),
    columns=['Enrolment\n(Normalized)', 'Updates\n(Normalized)', 'Risk Ratio\n(Normalized)'],
    index=top_20_states['state'].values
)

# Create heatmap
fig, ax = plt.subplots(figsize=(10, 12))

sns.heatmap(heatmap_data_normalized, 
            annot=True, 
            fmt='.2f', 
            cmap='coolwarm', 
            center=0.5,
            linewidths=1, 
            linecolor='white',
            cbar_kws={'label': 'Normalized Intensity (0=Low, 1=High)'},
            vmin=0, 
            vmax=1,
            ax=ax)

ax.set_title('State-wise Risk Heatmap: Top 20 States by Activity\nRed = High Risk/Volume | Blue = Low Risk/Volume', 
             fontweight='bold', fontsize=13, pad=20)
ax.set_xlabel('Metrics', fontweight='bold', fontsize=11)
ax.set_ylabel('State', fontweight='bold', fontsize=11)

# Rotate labels
plt.setp(ax.get_xticklabels(), rotation=0, ha='center')
plt.setp(ax.get_yticklabels(), rotation=0)

# Add color-coded risk indicators
for i, (idx, row) in enumerate(top_20_states.iterrows()):
    if row['Update_Ratio'] > upper_bound:
        ax.text(3.2, i + 0.5, '🚨', fontsize=12, va='center')
    elif row['Update_Ratio'] > merged_df['Update_Ratio'].quantile(0.75):
        ax.text(3.2, i + 0.5, '⚠️', fontsize=12, va='center')

plt.tight_layout()
output_path = os.path.join(output_dir, 'advanced_risk_heatmap.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"   ✓ Saved: {output_path}")
plt.close()

# ============================================================================
# VISUALIZATION 3: DUAL-AXIS COMBO CHART (Volume vs. Risk)
# ============================================================================
print("\n3. Creating Dual-Axis Combo Chart (Volume vs. Risk)...")

# Get top 10 states by Update Ratio
top_10_risk = merged_df.nlargest(10, 'Update_Ratio').copy()

fig, ax1 = plt.subplots(figsize=(14, 8))

# Create bar chart for Enrolment Count (left Y-axis)
x_pos = np.arange(len(top_10_risk))
bars = ax1.bar(x_pos, top_10_risk['Enrolment_Count'], 
               color='steelblue', alpha=0.7, edgecolor='darkblue', linewidth=1.5,
               label='Enrolment Count', width=0.6)

ax1.set_xlabel('State', fontweight='bold', fontsize=12)
ax1.set_ylabel('Enrolment Count', color='steelblue', fontweight='bold', fontsize=12)
ax1.tick_params(axis='y', labelcolor='steelblue')
ax1.set_xticks(x_pos)
ax1.set_xticklabels(top_10_risk['state'], rotation=45, ha='right')
ax1.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for i, bar in enumerate(bars):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height):,}',
             ha='center', va='bottom', fontsize=8, color='darkblue', fontweight='bold')

# Create second Y-axis for Update Ratio (line chart)
ax2 = ax1.twinx()
line = ax2.plot(x_pos, top_10_risk['Update_Ratio'], 
                color='red', marker='o', markersize=10, linewidth=3,
                label='Update Ratio', markeredgecolor='darkred', markeredgewidth=2)

ax2.set_ylabel('Update-to-Enrolment Ratio', color='red', fontweight='bold', fontsize=12)
ax2.tick_params(axis='y', labelcolor='red')

# Add value labels on line points
for i, (x, y) in enumerate(zip(x_pos, top_10_risk['Update_Ratio'])):
    ax2.annotate(f'{y:.1f}', 
                 xy=(x, y), 
                 xytext=(0, 10),
                 textcoords='offset points',
                 ha='center',
                 fontsize=9,
                 color='darkred',
                 fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

# Add threshold line
ax2.axhline(y=upper_bound, color='orange', linestyle='--', linewidth=2, 
            alpha=0.7, label=f'Outlier Threshold ({upper_bound:.1f})')

# Title and legends
plt.title('Volume vs. Risk: Enrolment Counts and Update Ratios\nTop 10 States by Update Ratio', 
          fontweight='bold', fontsize=14, pad=20)

# Combine legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', framealpha=0.9, fontsize=10)

# Add interpretation box
interpretation = "High bars + High line = High volume with high risk\nLow bars + High line = Low volume but high risk (investigate!)"
ax1.text(0.98, 0.02, interpretation, transform=ax1.transAxes, fontsize=9,
         verticalalignment='bottom', horizontalalignment='right',
         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

plt.tight_layout()
output_path = os.path.join(output_dir, 'advanced_combo_chart.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"   ✓ Saved: {output_path}")
plt.close()

# STEP 3: SUMMARY REPORT
print("\n" + "="*70)
print("ADVANCED ANALYSIS COMPLETE!")
print("="*70)

print("\n📊 VISUALIZATIONS CREATED:")
print(f"  1. {os.path.join(output_dir, 'advanced_boxplot_outliers.png')} - Statistical outlier detection")
print(f"  2. {os.path.join(output_dir, 'advanced_risk_heatmap.png')} - Top 20 states risk intensity")
print(f"  3. {os.path.join(output_dir, 'advanced_combo_chart.png')} - Volume vs. risk correlation")

print("\n🔍 KEY INSIGHTS:")
print(f"\n  Statistical Outliers Detected: {len(outliers)}")
print(f"  Outlier Threshold (IQR Method): {upper_bound:.2f}")
print(f"\n  Top 5 High-Risk States:")
for i, row in merged_df.head(5).iterrows():
    risk_level = "🚨 CRITICAL" if row['Update_Ratio'] > upper_bound else "⚠️ HIGH"
    print(f"    {i+1}. {row['state']:<35} Ratio: {row['Update_Ratio']:>6.2f}  {risk_level}")

print(f"\n  Correlation Analysis:")
correlation = top_10_risk['Enrolment_Count'].corr(top_10_risk['Update_Ratio'])
print(f"    Enrolment Count vs Update Ratio: {correlation:.3f}")
if abs(correlation) < 0.3:
    print(f"    → Weak correlation: High risk exists regardless of volume")
elif correlation > 0:
    print(f"    → Positive correlation: Higher volume = Higher risk")
else:
    print(f"    → Negative correlation: Higher volume = Lower risk")

print("\n📈 STATISTICAL SUMMARY:")
print(f"  Total States Analyzed: {len(merged_df)}")
print(f"  States Above Threshold: {len(merged_df[merged_df['Update_Ratio'] > upper_bound])}")
print(f"  States in Normal Range: {len(merged_df[merged_df['Update_Ratio'] <= upper_bound])}")
print(f"  Percentage Outliers: {(len(outliers)/len(merged_df)*100):.1f}%")

print("\n💡 RECOMMENDATIONS:")
print("  1. Investigate all states marked with 🚨 (critical outliers)")
print("  2. Review data quality for states with extreme ratios")
print("  3. Focus on low-volume, high-risk states (shown in combo chart)")
print("  4. Implement automated monitoring using these thresholds")

print("\n" + "="*70)
print("All visualizations saved at 300 DPI for publication quality!")
print("="*70)
