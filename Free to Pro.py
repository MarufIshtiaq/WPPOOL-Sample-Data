import pyodbc
import pandas as pd

server = 'DESKTOP-2LHRIRO'
database = 'wppool_sample_data'
driver = 'ODBC Driver 17 for SQL Server'

conn = pyodbc.connect(
    f'DRIVER={driver};'
    f'SERVER={server};'
    f'DATABASE={database};'
    'Trusted_Connection=yes'
)

sql_query = """
SELECT user_id, pro_upgrade_date, page_views
FROM wppool_data_sample
"""
df = pd.read_sql(sql_query, conn)

conn.close()

df = df.dropna(subset=['page_views'])

total_visitors = df['user_id'].nunique()

total_pro_upgrades = df['pro_upgrade_date'].count()

current_conversion_rate = total_pro_upgrades / total_visitors

new_conversion_rate = current_conversion_rate * 1.1

estimated_pro_upgrades = total_pro_upgrades * (new_conversion_rate / current_conversion_rate)

current_upgrade_percentage = current_conversion_rate * 100
estimated_upgrade_percentage = new_conversion_rate * 100

print(f"🔹 Total Visitors: {total_visitors}")
print(f"🔹 Current Pro Upgrades: {total_pro_upgrades}")
print(f"🔹 Current Upgrade Percentage: {current_upgrade_percentage:.2f}%")
print(f"🔹 Estimated Pro Upgrades after 10% conversion increase: {int(estimated_pro_upgrades)}")
print(f"🔹 Estimated Upgrade Percentage: {estimated_upgrade_percentage:.2f}%")