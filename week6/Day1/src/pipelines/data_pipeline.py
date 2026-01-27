import pandas as pd
import numpy as np

rawDataPath = '/home/prateek/Prateek/LaunchPad/week6/Day1/src/data/raw/data.csv'
PROCESSED_PATH = '/home/prateek/Prateek/LaunchPad/week6/Day1/src/data/processed'

DF = pd.read_csv(rawDataPath)

# droping unnecessary columns
DF.drop(columns=['PassengerId'], inplace=True)
DF.drop(columns=['Cabin'], inplace=True)
DF.drop(columns=['Name'], inplace=True)
DF.drop(columns=['Ticket'], inplace=True)

#handling missing values
DF['Age'] = DF['Age'].fillna(DF['Age'].mean())
DF['Embarked'] = DF['Embarked'].fillna(DF['Embarked'].mode()[0])

#label encoding
DF['Sex'] = DF['Sex'].map({'male': 1, 'female': 0})

#one-hot encoding
DF['Embarked_S'] = (DF['Embarked'] == 'S').astype(int)
DF['Embarked_C'] = (DF['Embarked'] == 'C').astype(int)
DF['Embarked_Q'] = (DF['Embarked'] == 'Q').astype(int)

#setting age to integer
DF['Age'] = DF['Age'].round().astype(int)

#now we can safely drop 'Embarked' column
DF.drop(columns=['Embarked'], inplace=True)

#after seeing correlation we can drop fare, sibsp, Embarked_Q and parch
DF.drop(columns=['Fare'], inplace=True)
DF.drop(columns=['SibSp'], inplace=True)
DF.drop(columns=['Embarked_Q'], inplace=True)
DF.drop(columns=['Parch'], inplace=True)

DF.to_csv(f'{PROCESSED_PATH}/final.csv', index=False)