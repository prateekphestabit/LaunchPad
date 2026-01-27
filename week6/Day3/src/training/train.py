import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from tensorflow import keras
from keras import layers
from keras.callbacks import EarlyStopping
from joblib import dump

# Load the dataset
df = pd.read_csv('/home/prateek/Prateek/LaunchPad/week6/Day3/src/data/processed/final.csv')

# Prepare the data
X = df.drop('Survived', axis=1).values
y = df['Survived'].values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Build the Neural Network model
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    layers.Dropout(0.3),
    layers.Dense(32, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(16, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Display model architecture
print("\n" + "="*50)
print("Model Architecture:")
print("="*50)
model.summary()

# Train the model with early stopping
early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=20,
    restore_best_weights=True
)

print("\n" + "="*50)
print("Training Model...")
print("="*50)
history = model.fit(
    X_train, y_train,
    epochs=100,
    batch_size=32,
    validation_split=0.2,
    callbacks=[early_stopping],
    verbose=1
)

print("\nTraining completed!")

# Plot training history
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot accuracy
axes[0].plot(history.history['accuracy'], label='Training Accuracy')
axes[0].plot(history.history['val_accuracy'], label='Validation Accuracy')
axes[0].set_title('Model Accuracy')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Accuracy')
axes[0].legend()
axes[0].grid(True)

# Plot loss
axes[1].plot(history.history['loss'], label='Training Loss')
axes[1].plot(history.history['val_loss'], label='Validation Loss')
axes[1].set_title('Model Loss')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Loss')
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.savefig('/home/prateek/Prateek/LaunchPad/week6/Day3/src/evaluation/training_history.png', dpi=300, bbox_inches='tight')
print("Training history plot saved to /home/prateek/Prateek/LaunchPad/week6/Day3/src/evaluation/training_history.png")
plt.show()

# Evaluate the model
print("\n" + "="*50)
print("Model Evaluation:")
print("="*50)
train_loss, train_accuracy = model.evaluate(X_train, y_train, verbose=0)
test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)

print(f"Training Accuracy: {train_accuracy:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f}")
print(f"Training Loss: {train_loss:.4f}")
print(f"Test Loss: {test_loss:.4f}")

# Make predictions
y_train_pred = (model.predict(X_train, verbose=0) > 0.5).astype(int).flatten()
y_test_pred = (model.predict(X_test, verbose=0) > 0.5).astype(int).flatten()

print("\n" + "="*50)
print("Classification Report (Test Set):")
print("="*50)
print(classification_report(y_test, y_test_pred))

# Calculate ROC-AUC
y_test_pred_proba = model.predict(X_test, verbose=0).flatten()
test_roc_auc = roc_auc_score(y_test, y_test_pred_proba)
print(f"\nTest ROC-AUC Score: {test_roc_auc:.4f}")

# Confusion Matrix
cm = confusion_matrix(y_test, y_test_pred)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True)
plt.title('Confusion Matrix - Neural Network')
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

# Save the model
models_dir = '/home/prateek/Prateek/LaunchPad/week6/Day3/src/models'
os.makedirs(models_dir, exist_ok=True)

h5_path = os.path.join(models_dir, 'neural_network_model.h5')
pkl_path = os.path.join(models_dir, 'best_model.pkl')

model.save(h5_path)
dump(model, pkl_path)

print("\n" + "="*50)
print(f"Model saved to {h5_path}")
print(f"Pickle saved to {pkl_path}")
print("="*50)
