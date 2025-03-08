import pyodbc
import pandas as pd
import numpy as np
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

sql_query = "SELECT * FROM wppool_data_sample"
df = pd.read_sql(sql_query, conn)

conn.close()

np.random.seed(42)
df["cta_color_group"] = np.random.choice(["A", "B"], size=len(df))

group_A_color = df[df["cta_color_group"] == "A"]
group_B_color = df[df["cta_color_group"] == "B"]

conversions_A_color = group_A_color["pro_upgrade_date"].notna().sum()
conversions_B_color = group_B_color["pro_upgrade_date"].notna().sum()

total_users_A_color = len(group_A_color)
total_users_B_color = len(group_B_color)

conversion_rate_A_color = (conversions_A_color / total_users_A_color) * 100
conversion_rate_B_color = (conversions_B_color / total_users_B_color) * 100

contingency_table_color = np.array([
    [conversions_A_color, total_users_A_color - conversions_A_color],
    [conversions_B_color, total_users_B_color - conversions_B_color]
])

chi2_color, p_color, dof_color, expected_color = stats.chi2_contingency(contingency_table_color)

print("\n🚀 CTA Color Variation Test")
print("Contingency Table (Color):\n", contingency_table_color)
print(f"Chi-Square Statistic (Color): {chi2_color:.2f}")
print(f"P-Value (Color): {p_color:.4f}")
print(f"Conversion Rate (Old Color): {conversion_rate_A_color:.2f}%")
print(f"Conversion Rate (New Color): {conversion_rate_B_color:.2f}%")

alpha = 0.05
if p_color < alpha:
    print("Result (Color): The new CTA color significantly increased conversions!")
else:
    print("Result (Color): No significant difference in CTA color. Try a different variation.")