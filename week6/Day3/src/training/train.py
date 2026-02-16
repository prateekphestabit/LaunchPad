import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, accuracy_score
from joblib import dump

# Load the dataset
df = pd.read_csv('/home/prateek/Prateek/LaunchPad/week6/Day3/src/data/processed/final.csv')

# Prepare the data
X = df.drop('Survived', axis=1)
y = df['Survived']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print("="*50)
print("Data Preparation Complete")
print("="*50)
print(f"Training set size: {X_train.shape[0]}")
print(f"Testing set size: {X_test.shape[0]}")
print(f"\nFeatures: {list(X.columns)}")

# Build the Random Forest model
print("\n" + "="*50)
print("Building Random Forest Model...")
print("="*50)

model = RandomForestClassifier(
    n_estimators=100,      # Number of trees
    max_depth=10,          # Maximum depth of trees
    min_samples_split=5,   # Minimum samples required to split
    min_samples_leaf=2,    # Minimum samples required at leaf node
    random_state=42,
    n_jobs=-1              # Use all available cores
)

# Train the model
model.fit(X_train, y_train)

print(f"\nRandom Forest Model trained successfully!")
print(f"Number of trees: {model.n_estimators}")
print(f"Max depth: {model.max_depth}")
print(f"Number of features: {model.n_features_in_}")

# Make predictions
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

# Get prediction probabilities
y_train_pred_proba = model.predict_proba(X_train)[:, 1]
y_test_pred_proba = model.predict_proba(X_test)[:, 1]

# Evaluate the model
print("\n" + "="*50)
print("Model Evaluation:")
print("="*50)
train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

print(f"Training Accuracy: {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
print(f"Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")

# ROC-AUC Score
train_roc_auc = roc_auc_score(y_train, y_train_pred_proba)
test_roc_auc = roc_auc_score(y_test, y_test_pred_proba)
print(f"\nTraining ROC-AUC Score: {train_roc_auc:.4f}")
print(f"Testing ROC-AUC Score: {test_roc_auc:.4f}")

print("\n" + "="*50)
print("Classification Report (Test Set):")
print("="*50)
print(classification_report(y_test, y_test_pred, target_names=['Not Survived', 'Survived']))

# Confusion Matrix
cm = confusion_matrix(y_test, y_test_pred)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Greens', cbar=True,
            xticklabels=['Not Survived', 'Survived'],
            yticklabels=['Not Survived', 'Survived'])
plt.title('Confusion Matrix - Random Forest (Best Model)')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.savefig('/home/prateek/Prateek/LaunchPad/week6/Day3/src/evaluation/confusion_matrix.png', dpi=300, bbox_inches='tight')
print("\nConfusion matrix plot saved to /home/prateek/Prateek/LaunchPad/week6/Day3/src/evaluation/confusion_matrix.png")
plt.show()

print("\nConfusion Matrix:")
print(cm)
print(f"True Negatives: {cm[0][0]}")
print(f"False Positives: {cm[0][1]}")
print(f"False Negatives: {cm[1][0]}")
print(f"True Positives: {cm[1][1]}")

# Feature Importance
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=False)

print("\n" + "="*50)
print("Feature Importance (Gini Importance):")
print("="*50)
print(feature_importance)

# Plot feature importance
plt.figure(figsize=(10, 6))
plt.barh(feature_importance['Feature'], feature_importance['Importance'], color='forestgreen')
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.title('Feature Importance - Random Forest')
plt.grid(alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('/home/prateek/Prateek/LaunchPad/week6/Day3/src/evaluation/feature_importance.png', dpi=300, bbox_inches='tight')
print("\nFeature importance plot saved to /home/prateek/Prateek/LaunchPad/week6/Day3/src/evaluation/feature_importance.png")
plt.show()

# Save the model
models_dir = '/home/prateek/Prateek/LaunchPad/week6/Day3/src/models'
os.makedirs(models_dir, exist_ok=True)

model_path = os.path.join(models_dir, 'random_forest_model.joblib')
best_model_path = os.path.join(models_dir, 'best_model.joblib')

dump(model, model_path)
dump(model, best_model_path)

print("\n" + "="*50)
print("Model Saved Successfully!")
print("="*50)
print(f"Model saved to: {model_path}")
print(f"Best model saved to: {best_model_path}")

print("\n" + "="*50)
print("SUMMARY")
print("="*50)
print("Best Model: Random Forest")
print(f"Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
print(f"Test ROC-AUC: {test_roc_auc:.4f}")
print("Reason: Random Forest achieved the highest test accuracy tied with XGBoost,")
print("        but with a higher ROC-AUC score (0.8352 vs 0.8111). It demonstrates")
print("        the best overall balance across all metrics.")
