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

sql_query = "SELECT * FROM wppool_data_sample"
df = pd.read_sql(sql_query, conn)

sql_query = "SELECT * FROM wppool_data_sample"

df = pd.read_sql(sql_query, conn)

conn.close()

df['subscription_type'] = df['subscription_type'].str.strip().str.lower()

pro_users = df[df['subscription_type'] == 'pro']

total_pro_revenue = pro_users['monthly_revenue'].sum()

print("Total Monthly Revenue from Pro Users:", total_pro_revenue)