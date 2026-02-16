# Model Comparison Report

## Pipeline Flow
```
data_pipeline.py ==> build_features.py ==> feature_selector.py ==> train.py
```

## Dataset
- **Dataset**: Titanic Survival Prediction
- **Total Samples**: 891
- **Features**: Pclass, Sex, Age, Embarked_S, Embarked_C
- **Target**: Survived (Binary Classification)
- **Train/Test Split**: 80/20 (712 train, 179 test)

## Model Performance Summary

| Model | Test Accuracy | Test ROC-AUC | Weighted F1 | Weighted Precision | Weighted Recall |
|-------|--------------|--------------|-------------|--------------------|-----------------| 
| **Random Forest** | **78.77%** | 0.8352 | **0.78** | 0.79 | 0.79 |
| XGBoost | 78.77% | 0.8111 | 0.78 | 0.79 | 0.79 |
| Neural Network | 78.21% | **0.8457** | 0.76 | 0.81 | 0.78 |
| Logistic Regression | 76.54% | 0.8329 | 0.76 | 0.76 | 0.77 |

## Detailed Results

### 1. Random Forest (Best Model) 
- **Test Accuracy**: 78.77%
- **Test ROC-AUC**: 0.8352
- **Training Accuracy**: 87.64%
- **Configuration**:
  - n_estimators: 100
  - max_depth: 10
  - min_samples_split: 5
  - min_samples_leaf: 2

**Classification Report:**
```
              precision    recall  f1-score   support
Not Survived       0.80      0.87      0.83       110
    Survived       0.76      0.65      0.70        69
    accuracy                           0.79       179
weighted avg       0.79      0.79      0.78       179
```

### 2. XGBoost
- **Test Accuracy**: 78.77%
- **Test ROC-AUC**: 0.8111
- **Training Accuracy**: 86.80%
- **Configuration**:
  - n_estimators: 100
  - learning_rate: 0.1
  - max_depth: 5

**Classification Report:**
```
              precision    recall  f1-score   support
           0       0.80      0.88      0.84       110
           1       0.77      0.64      0.70        69
    accuracy                           0.79       179
weighted avg       0.79      0.79      0.78       179
```

### 3. Neural Network
- **Test Accuracy**: 78.21%
- **Test ROC-AUC**: 0.8457
- **Training Accuracy**: 79.92%
- **Architecture**:
  - Dense(64, relu) → Dropout(0.3)
  - Dense(32, relu) → Dropout(0.3)
  - Dense(16, relu) → Dropout(0.2)
  - Dense(1, sigmoid)

**Classification Report:**
```
              precision    recall  f1-score   support
           0       0.75      0.97      0.85       110
           1       0.92      0.48      0.63        69
    accuracy                           0.78       179
weighted avg       0.81      0.78      0.76       179
```

### 4. Logistic Regression
- **Test Accuracy**: 76.54%
- **Test ROC-AUC**: 0.8329
- **Training Accuracy**: 79.49%

**Classification Report:**
```
              precision    recall  f1-score   support
Not Survived       0.80      0.83      0.81       110
    Survived       0.71      0.67      0.69        69
    accuracy                           0.77       179
weighted avg       0.76      0.77      0.76       179
```

## Rankings

### By Accuracy
1. Random Forest: 78.77%
2. XGBoost: 78.77%
3. Neural Network: 78.21%
4. Logistic Regression: 76.54%

### By ROC-AUC
1. Neural Network: 0.8457
2. Random Forest: 0.8352
3. Logistic Regression: 0.8329
4. XGBoost: 0.8111

### By Weighted F1-Score
1. Random Forest: 0.78
2. XGBoost: 0.78
3. Logistic Regression: 0.76
4. Neural Network: 0.76

## Best Model Selection

### Winner: Random Forest 

