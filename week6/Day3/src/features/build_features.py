import pandas as pd
import numpy as np

PROCESSED_PATH = '/home/prateek/Prateek/LaunchPad/week6/Day2/src/data/processed/final.csv'

DF = pd.read_csv(PROCESSED_PATH)

#label encoding
DF['Sex'] = DF['Sex'].map({'male': 1, 'female': 0})

#one-hot encoding
DF['Embarked_S'] = (DF['Embarked'] == 'S').astype(int)
DF['Embarked_C'] = (DF['Embarked'] == 'C').astype(int)
DF['Embarked_Q'] = (DF['Embarked'] == 'Q').astype(int)

DF.to_csv(PROCESSED_PATH, index=False)