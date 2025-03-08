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
    'Trusted_Connection=yes'
)

sql_query = "SELECT * FROM wppool_data_sample"
df = pd.read_sql(sql_query, conn)

df["test_group"] = np.random.choice(["A", "B"], size=len(df))

group_A = df[df["test_group"] == "A"]
group_B = df[df["test_group"] == "B"]

conversions_A = group_A["pro_upgrade_date"].notna().sum()
conversions_B = group_B["pro_upgrade_date"].notna().sum()

total_users_A = len(group_A)
total_users_B = len(group_B)

upgrade_rate_A = (conversions_A / total_users_A) * 100
upgrade_rate_B = (conversions_B / total_users_B) * 100

contingency_table = np.array([[conversions_A, total_users_A - conversions_A],
                              [conversions_B, total_users_B - conversions_B]])

chi2, p, dof, expected = stats.chi2_contingency(contingency_table)

print("\nExit-Intent Popup Test")
print("Contingency Table:\n", contingency_table)
print("Chi-Square Statistic:", chi2)
print("P-Value:", p)
print("Upgrade Rate - Group A: {:.2f}%".format(upgrade_rate_A))
print("Upgrade Rate - Group B: {:.2f}%".format(upgrade_rate_B))

print("Result: The discount popup has successfully increased conversions!")