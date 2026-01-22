import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configuration ---
file_path = 'scholarship_results.csv'

# --- 1. Load Data and Feature Engineering ---
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
    exit()

# Extract Academic Tier, Financial Level, and Activity Level from the 'Explanation' column
# The 'Explanation' column has the format: "Academic: [level], Financial: [level], Activities: [level], ..."
df['Academic_Tier'] = df['Explanation'].str.extract(r'Academic: (\w+)')
df['Financial_Level'] = df['Explanation'].str.extract(r'Financial: (\w+)')
df['Activity_Level'] = df['Explanation'].str.extract(r'Activities: (\w+)')

# Filter the data for visualization 3, 4, and 5: Keep only competitive applicants 
# (i.e., those not marked as 'Not Eligible - Basic Requirements' which have Confidence > 0)
df_filtered = df[df['Academic_Tier'].notna() & (df['Confidence'] > 0)].copy()

print("Data loaded and features extracted successfully.")

# --- 2. Visualization Functions ---

# --- CHART 1: Distribution of Decisions (On the full dataset) ---
plt.figure(figsize=(10, 6))
decision_counts = df['Decision'].value_counts()
sns.countplot(data=df, y='Decision', order=decision_counts.index, palette='viridis')
plt.title('1. Distribution of Scholarship Decisions')
plt.xlabel('Number of Students')
plt.ylabel('Decision')
plt.tight_layout()
plt.savefig('decision_distribution_chart.png')
plt.close()

# --- CHART 2: Confidence Score Distribution by Decision (On the full dataset) ---
plt.figure(figsize=(12, 7))
sns.boxplot(x='Decision', y='Confidence', data=df, palette='Set2')
plt.title('2. Confidence Score Distribution Grouped by Decision')
plt.xlabel('Decision')
plt.ylabel('Confidence Score')
plt.tight_layout()
plt.savefig('confidence_by_decision_boxplot.png')
plt.close()

# --- CHART 3: Decision Breakdown by Academic Tier (On filtered dataset) ---
decision_by_tier = pd.crosstab(df_filtered['Academic_Tier'], df_filtered['Decision'])
plt.figure(figsize=(10, 6))
# Define order for academic tiers
tier_order = ['tier1', 'tier2', 'tier3']
decision_by_tier.reindex(tier_order, fill_value=0).plot(kind='bar', stacked=True, figsize=(10, 6), colormap='tab10', ax=plt.gca())
plt.title('3. Scholarship Decisions Broken Down by Academic Tier')
plt.xlabel('Academic Tier')
plt.ylabel('Number of Students')
plt.xticks(rotation=0)
plt.legend(title='Decision')
plt.tight_layout()
plt.savefig('decision_by_academic_tier_stacked_bar.png')
plt.close()

# --- CHART 4: Decision Breakdown by Financial Level (On filtered dataset) ---
decision_by_financial = pd.crosstab(df_filtered['Financial_Level'], df_filtered['Decision'])
plt.figure(figsize=(10, 6))
# Define order for financial levels
financial_order = ['minimal', 'medium', 'high']
decision_by_financial.reindex(financial_order, fill_value=0).plot(kind='bar', stacked=True, figsize=(10, 6), colormap='plasma', ax=plt.gca())
plt.title('4. Scholarship Decisions Broken Down by Financial Level')
plt.xlabel('Financial Level')
plt.ylabel('Number of Students')
plt.xticks(rotation=0)
plt.legend(title='Decision')
plt.tight_layout()
plt.savefig('decision_by_financial_level_stacked_bar.png')
plt.close()

# --- CHART 5: Decision Breakdown by Activity Level (On filtered dataset) ---
decision_by_activity = pd.crosstab(df_filtered['Activity_Level'], df_filtered['Decision'])
plt.figure(figsize=(10, 6))
# Define order for activity levels
activity_order = ['poor', 'basic', 'moderate', 'strong', 'outstanding']
decision_by_activity.reindex(activity_order, fill_value=0).plot(kind='bar', stacked=True, figsize=(10, 6), colormap='Set1', ax=plt.gca())
plt.title('5. Scholarship Decisions Broken Down by Activity Level')
plt.xlabel('Activity Level')
plt.ylabel('Number of Students')
plt.xticks(rotation=0)
plt.legend(title='Decision')
plt.tight_layout()
plt.savefig('decision_by_activity_level_stacked_bar.png')
plt.close()

print("\nAll 5 visualization files have been saved in the current directory.")