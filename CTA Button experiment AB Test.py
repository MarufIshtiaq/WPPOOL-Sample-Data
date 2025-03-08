import pyodbc
import numpy as np
import pandas as pd
import scipy.stats as stats

server = 'DESKTOP-2LHRIRO'
database = 'wppool_sample_data'
driver = 'ODBC Driver 17 for SQL Server'

conn = pyodbc.connect(
    f'DRIVER={driver};'
    f'SERVER={server};'
    f'DATABASE={database};'
    'Trusted_Connection=yes;'
)

df = pd.read_sql("SELECT * FROM wppool_data_sample", conn)
conn.close()

df["test_group"] = np.random.choice(["A", "B"], size=len(df))

group_A = df[df["test_group"] == "A"]
group_B = df[df["test_group"] == "B"]

conversions_A = group_A["pro_upgrade_date"].notna().sum()
conversions_B = group_B["pro_upgrade_date"].notna().sum()

total_users_A = len(group_A)
total_users_B = len(group_B)

contingency_table = np.array([[conversions_A, total_users_A - conversions_A],
                              [conversions_B, total_users_B - conversions_B]])

chi2, p, dof, expected = stats.chi2_contingency(contingency_table)

print("\nCTA Button Optimization Test")
print("Contingency Table:\n", contingency_table)
print("Chi-Square Statistic:", chi2)
print("P-Value:", p)

alpha = 0.05
if p < alpha:
    print("Result: The new CTA button significantly increased conversions!")
else:
    print("Result: No significant difference. Try a different CTA variation.")