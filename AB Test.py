import pyodbc
import pandas as pd
import scipy.stats as stats

server = 'DESKTOP-2LHRIRO'
database = 'wppool_sample_data'
driver = 'ODBC Driver 17 for SQL Server'

try:
    conn = pyodbc.connect(
        f'DRIVER={driver};'
        f'SERVER={server};'
        f'DATABASE={database};'
        'Trusted_Connection=yes'
    )
    print("Connected to SQL Server successfully!")
except Exception as e:
    print("Error connecting to SQL Server:", e)
    exit()

query = """
SELECT 
    subscription_type AS subscription_group, 
    churned AS converted, 
    monthly_revenue 
FROM wppool_data_sample
"""
df = pd.read_sql(query, conn)

conn.close()

print("Columns in dataset:", df.columns)
print("First few rows:\n", df.head())

print("\nUnique values in 'subscription_group':", df['subscription_group'].unique())
print("Unique values in 'converted':", df['converted'].unique())

df['converted'] = df['converted'].map({'Yes': 1, 'No': 0, 1: 1, 0: 0})
df = df.dropna(subset=['subscription_group', 'converted'])

df['subscription_group'] = df['subscription_group'].str.strip().str.lower()

pro_users = df[df['subscription_group'] == 'pro']
total_pro_revenue = pro_users['monthly_revenue'].sum()
print("Total Monthly Revenue from Pro Users:", total_pro_revenue)

contingency_table = pd.crosstab(df['subscription_group'], df['converted'])

if contingency_table.empty:
    raise ValueError("Contingency table is empty. Check your data!")

chi2, p, dof, expected = stats.chi2_contingency(contingency_table)

print("\nContingency Table:\n", contingency_table)
print("\nChi-Square Statistic:", chi2)
print("P-Value:", p)

alpha = 0.05
if p < alpha:
    print("\nThere is a significant difference in conversion rates between groups.")
else:
    print("\nNo significant difference found in conversion rates between groups.")