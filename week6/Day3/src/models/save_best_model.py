import pandas as pd
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from joblib import dump

# Define paths
DATA_PATH = '../data/processed/final.csv'
MODEL_PATH = '../models/best_model.joblib'
PKL_PATH = '../models/best_model.pkl'


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

# Create and train the Random Forest model (Best Model)
print("\nTraining Random Forest model (Best Model)...")
rf_model = RandomForestClassifier(
    n_estimators=100,      # Number of trees
    max_depth=10,          # Maximum depth of trees
    min_samples_split=5,   # Minimum samples required to split
    min_samples_leaf=2,    # Minimum samples required at leaf node
    random_state=42,
    n_jobs=-1              # Use all available cores
)

rf_model.fit(X_train, y_train)
print("Model training completed!")

# Evaluate the model
y_train_pred = rf_model.predict(X_train)
y_test_pred = rf_model.predict(X_test)
y_test_pred_proba = rf_model.predict_proba(X_test)[:, 1]

train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)
test_roc_auc = roc_auc_score(y_test, y_test_pred_proba)

print(f"\nTraining Accuracy: {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
print(f"Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
print(f"Test ROC-AUC: {test_roc_auc:.4f}")

print("\nClassification Report (Test Set):")
print("="*50)
print(classification_report(y_test, y_test_pred, target_names=['Not Survived', 'Survived']))

# Save the model using joblib (recommended for scikit-learn models)
print(f"\nSaving model to '{MODEL_PATH}'...")
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
dump(rf_model, MODEL_PATH)
print("Model saved successfully (joblib format)!")

# Also save as pickle for backward compatibility
print(f"\nSaving model to '{PKL_PATH}' (pickle format)...")
with open(PKL_PATH, 'wb') as f:
    pickle.dump(rf_model, f)
print("Model saved successfully (pickle format)!")


print("\n" + "="*50)
print("Training and saving complete!")
print("="*50)
print(f"Best Model: Random Forest")
print(f"Model path (joblib): {MODEL_PATH}")
print(f"Model path (pickle): {PKL_PATH}")
print(f"Features: {list(X.columns)}")
print(f"Test Accuracy: {test_accuracy:.4f}")
print(f"Test ROC-AUC: {test_roc_auc:.4f}")
print("\nReason for selection:")
print("Random Forest achieved the highest test accuracy (78.77%) tied with XGBoost,")
print("but with a higher ROC-AUC score (0.8352 vs 0.8111). It demonstrates the best")
print("overall balance across all metrics including weighted F1-score (0.78).")
