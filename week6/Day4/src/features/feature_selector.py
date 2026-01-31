import pandas as pd
import numpy as np
import json

PROCESSED_PATH = '/home/prateek/Prateek/LaunchPad/week6/Day2/src/data/processed/final.csv'
FEATURE_LIST_PATH = '/home/prateek/Prateek/LaunchPad/week6/Day2/src/features/feature_list.json'

DF = pd.read_csv(PROCESSED_PATH)

#now we can safely drop features after reviewing EDA
DF.drop(columns=['Embarked'], inplace=True)
DF.drop(columns=['Fare'], inplace=True)
DF.drop(columns=['SibSp'], inplace=True)
DF.drop(columns=['Embarked_Q'], inplace=True)
DF.drop(columns=['Parch'], inplace=True)

#Normalizes numerical features
numeric_cols = DF.select_dtypes(include=[np.number]).columns.tolist()
continuous_cols = [c for c in numeric_cols if c != 'Survived' and DF[c].nunique() > 10]

for c in continuous_cols:
    cmin, cmax = DF[c].min(), DF[c].max()
    if cmax > cmin:
        DF[c] = (DF[c] - cmin) / (cmax - cmin)

DF.to_csv(PROCESSED_PATH, index=False)

# Generate feature_list.json automatically
feature_list = {
    "features": [],
    "total_samples": len(DF),
    "total_features": len(DF.columns)
}

for col in DF.columns:
    feature_info = {
        "name": col,
        "dtype": str(DF[col].dtype),
        "non_null_count": int(DF[col].notna().sum()),
        "type": "target" if col == "Survived" else ("categorical" if "Embarked" in col or col in ["Pclass", "Sex"] else "numerical"),
        "description": f"Feature: {col}"
    }
    feature_list["features"].append(feature_info)

# Save to JSON
with open(FEATURE_LIST_PATH, 'w') as f:
    json.dump(feature_list, f, indent=2)
