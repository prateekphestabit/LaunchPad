import pandas as pd
import pickle
import os
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Define paths
DATA_PATH = '../data/processed/final.csv'
MODEL_PATH = '../models/best_model.pkl'
FEATURES_PATH = '../models/feature_names.pkl'

# Load the dataset
print("Loading dataset...")
df = pd.read_csv(DATA_PATH)
print(f"Dataset loaded: {df.shape[0]} samples, {df.shape[1]} features")

# Prepare the data
X = df.drop('Survived', axis=1)
y = df['Survived']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\nTraining set: {X_train.shape[0]} samples")
print(f"Test set: {X_test.shape[0]} samples")

# Create and train the XGBoost model
print("\nTraining XGBoost model...")
xgb_model = XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42,
    eval_metric='logloss'
)

xgb_model.fit(X_train, y_train)
print("Model training completed!")

# Evaluate the model
y_train_pred = xgb_model.predict(X_train)
y_test_pred = xgb_model.predict(X_test)

train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

print(f"\nTraining Accuracy: {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
print(f"Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")

print("\nClassification Report (Test Set):")
print("="*50)
print(classification_report(y_test, y_test_pred, target_names=['Not Survived', 'Survived']))

# Save the model
print(f"\nSaving model to '{MODEL_PATH}'...")
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
with open(MODEL_PATH, 'wb') as f:
    pickle.dump(xgb_model, f)
print("Model saved successfully!")

# Save feature names for later use
print("\nSaving feature names...")
with open(FEATURES_PATH, 'wb') as f:
    pickle.dump(list(X.columns), f)
print("Feature names saved!")

print("\n" + "="*50)
print("Training and saving complete!")
print("="*50)
print(f"Model path: {MODEL_PATH}")
print(f"Features: {list(X.columns)}")
print(f"Test Accuracy: {test_accuracy:.4f}")
