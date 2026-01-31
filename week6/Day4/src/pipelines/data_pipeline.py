import pandas as pd
import numpy as np

rawDataPath = '/home/prateek/Prateek/LaunchPad/week6/Day2/src/data/raw/data.csv'
PROCESSED_PATH = '/home/prateek/Prateek/LaunchPad/week6/Day2/src/data/processed'

DF = pd.read_csv(rawDataPath)

# droping unnecessary columns
DF.drop(columns=['PassengerId'], inplace=True)
DF.drop(columns=['Name'], inplace=True)
DF.drop(columns=['Ticket'], inplace=True)

#dropping cabin due to high missing values
DF.drop(columns=['Cabin'], inplace=True)

#handling missing values
DF['Age'] = DF['Age'].fillna(DF['Age'].mean())
DF['Embarked'] = DF['Embarked'].fillna(DF['Embarked'].mode()[0])

DF.to_csv(f'{PROCESSED_PATH}/final.csv', index=False)