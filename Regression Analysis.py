import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

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

df['install_date'] = pd.to_datetime(df['install_date'], errors='coerce')
df['last_active_date'] = pd.to_datetime(df['last_active_date'], errors='coerce')
df['pro_upgrade_date'] = pd.to_datetime(df['pro_upgrade_date'], errors='coerce')

df = df.drop(columns=['user_id', 'install_date', 'last_active_date', 'pro_upgrade_date'])

df = pd.get_dummies(df, columns=['subscription_type', 'country', 'plan_type'], drop_first=True)

X = df.drop(columns=['churned'])
y = df['churned']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

log_reg = LogisticRegression()
log_reg.fit(X_train, y_train)

y_pred = log_reg.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print("Classification Report:\n", classification_report(y_test, y_pred))

feature_importance = pd.Series(log_reg.coef_[0], index=X.columns).sort_values(key=abs, ascending=False)
print("\nFeature Importance:\n", feature_importance)

top_3_features = feature_importance[:3]
print("\nTop 3 Reasons for Churn:")
for feature, coef in top_3_features.items():
    print(f"{feature}: {coef}")

plt.figure(figsize=(8, 4))
top_3_features.plot(kind='bar', color='red')
plt.title("Top 3 Factors Influencing Churn")
plt.xlabel("Features")
plt.ylabel("Coefficient Value")
plt.xticks(rotation=45)
plt.show()