import pickle
import numpy as np
import os
import csv
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel

# Load the trained model - use environment variable or default path
MODEL_PATH = os.getenv("MODEL_PATH", "/home/prateek/Prateek/LaunchPad/week6/Day5/src/models/best_model.pkl")
LOG_PATH = os.getenv("LOG_PATH", "/home/prateek/Prateek/LaunchPad/week6/Day5/src/deployment/prediction_logs.csv")

with open(MODEL_PATH, "rb") as f:
    clf = pickle.load(f)

# try to change name from IrisFeatures to TitanicFeatures
class TitanicFeatures(BaseModel):
    Pclass: int
    Sex: int
    Age: float
    Embarked_S: int
    Embarked_C: int


# Create FastAPI instance
app = FastAPI()

# Define prediction endpoint
@app.post("/predict")
def predict(data: TitanicFeatures):
    test_data = np.array([[
        data.Pclass,
        data.Sex,
        data.Age,
        data.Embarked_S,
        data.Embarked_C
    ]])
    prediction = clf.predict(test_data)[0]
    # For binary classification, convert probability to class
    predicted_class = int(prediction[0] > 0.5)
    probability = float(prediction[0])
    
    # Log prediction to CSV
    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            data.Pclass,
            data.Sex,
            data.Age,
            data.Embarked_S,
            data.Embarked_C,
            predicted_class,
            probability
        ])
    
    return {"prediction": predicted_class, "probability": probability}