import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn import preprocessing, model_selection
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

from src.main.core import myconfig
from src.main.core import invesco
import os

dataset = myconfig.PROCESSED_DATASET_FOLDER + myconfig.SEP + 'dataset.csv'
df = invesco._load_df(dataset)

# Filtering Tnx Dataframe for the required values only.
df.drop(['Unique_Advisor_Id', 'Unique_Investment_Id', 'Month'], 1, inplace=True)

x = np.array(df.drop(['class_label'], 1))
y = np.array(df['class_label'])

x_train, x_test, y_train, y_test = model_selection.train_test_split(x, y, test_size=0.3)

model2 = LogisticRegression()
model2.fit(x_train, y_train)

accuracy = model2.score(x_test, y_test)
print(accuracy)
