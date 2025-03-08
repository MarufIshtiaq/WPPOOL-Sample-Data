import pyodbc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

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

print(df.head())
print(df.info())

df['install_date'] = pd.to_datetime(df['install_date'])
df['pro_upgrade_date'] = pd.to_datetime(df['pro_upgrade_date'])

df['upgraded_to_pro'] = (df['subscription_type'] == 'Pro').astype(int)

df['days_to_upgrade'] = (df['pro_upgrade_date'] - df['install_date']).dt.days

features = ['total_sessions', 'page_views', 'days_active']
target = 'upgraded_to_pro'

print(df[features].isnull().sum())
df = df.dropna(subset=features)

X = df[features]
y = df[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = LogisticRegression()
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)

accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')
print(classification_report(y_test, y_pred))

conf_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

sns.histplot(df['days_to_upgrade'].dropna(), bins=30, kde=True)
plt.xlabel('Days to Upgrade')
plt.ylabel('Frequency')
plt.title('Distribution of Days to Upgrade')
plt.show()

country_upgrade_stats = df.groupby('country')['days_to_upgrade'].mean().dropna().sort_values()
plt.figure(figsize=(12, 6))
sns.barplot(x=country_upgrade_stats.index, y=country_upgrade_stats.values)
plt.xticks(rotation=90)
plt.xlabel('Country')
plt.ylabel('Average Days to Upgrade')
plt.title('Average Days to Upgrade by Country')
plt.show()