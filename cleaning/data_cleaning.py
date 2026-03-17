import pandas as pd
import numpy as np
from google.colab import files
#Q1: Load dataset & initial exploration
uploaded = files.upload()
filename = list(uploaded.keys())[0]
df = pd.read_csv(filename)
import numpy as np
np.random.seed(42)
print("Shape:", df.shape)
print("\nColumn Names:\n", df.columns.tolist())
print("\nData Types:\n", df.dtypes)
print("\nFirst 5 Rows:\n", df.head())
# Q2: Drop unnecessary columns & remove duplicates

# Drop unnecessary columns
cols_to_drop = ["Unnamed: 0", "v10", "v2.5", "nv10", "nv2.5", "no"]
df = df.drop(columns=cols_to_drop, errors="ignore")
print("Columns after drop:", df.columns.tolist())

# Remove duplicate rows
before = len(df)
df = df.drop_duplicates()
print(f"Duplicates removed: {before - len(df)}")
print("Remaining rows:", len(df))
print(f"Duplicates removed: {before - len(df)}")
print("Remaining rows:", len(df))
# Q3: Parse dates & extract time features

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"])

# Extract time features
df["year"]  = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day"]   = df["date"].dt.day
df["hour"]  = df["date"].dt.hour

print("Sample date features:")
print(df[["date", "year", "month", "day", "hour"]].head())
# Q4: Handle missing values
print("Missing Values Before:\n", df.isnull().sum())
# Fill numeric columns with median
numeric_cols = df.select_dtypes(include=np.number).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

# Drop rows where critical pollutant columns are still missing
df = df.dropna(subset=["pm25", "pm10", "no2"])

print("\nMissing Values After:\n", df.isnull().sum())
# Q5: Remove outliers using IQR

# Calculate All boundaries first before removing anything
bounds = {}

for col in ["pm25", "pm10", "no2", "o3", "so2"]:
    Q1  = df[col].quantile(0.25)
    Q3  = df[col].quantile(0.75)
    IQR = Q3 - Q1
    bounds[col] = {
        "lower": Q1 - 1.5 * IQR,
        "upper": Q3 + 1.5 * IQR
    }

# Filter all at once
before = len(df)

for col, b in bounds.items():
    df = df[(df[col] >= b["lower"]) & (df[col] <= b["upper"])]

print(f"Total outliers removed: {before - len(df)}")
print(f"Final shape: {df.shape}")

# Add season column
def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Autumn"

df["season"] = df["month"].apply(get_season)
print("\nSeason counts:\n", df["season"].value_counts())

# Add AQI category column
def aqi_category(pm25):
    if pm25 <= 11:
        return "Low"
    elif pm25 <= 23:
        return "Moderate"
    elif pm25 <= 35:
        return "High"
    else:
        return "Very High"

df["aqi_category"] = df["pm25"].apply(aqi_category)
print("\nAQI category counts:\n", df["aqi_category"].value_counts())

# Summary
print("\nCleaned Dataset Summary")
print(f"Total records  : {len(df)}")
print(f"Date range     : {df['date'].min()} to {df['date'].max()}")
print(f"Sites covered  : {df['site'].nunique()}")
print(f"Avg PM2.5      : {df['pm25'].mean():.2f} µg/m³")
print(f"Avg NO2        : {df['no2'].mean():.2f} µg/m³")

# Save cleaned file
df.to_csv("UK_Air_Quality_Cleaned.csv", index=False)
print("Cleaned dataset saved. Final shape:", df.shape)
