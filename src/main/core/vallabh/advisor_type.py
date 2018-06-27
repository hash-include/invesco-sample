import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import os

current_dir = os.path.realpath(__file__)
RESOURCE_FOLDER = os.sep.join(current_dir.split(os.sep)[:-2]) + os.sep + "resources"
DATASET_FOLDER = RESOURCE_FOLDER + os.sep + "dataset"
DATA_ACTIVITY_PATH = DATASET_FOLDER + os.sep + "Activity.csv"
DATA_AUM_PATH = DATASET_FOLDER + os.sep + "AUM.csv"
DATA_INVEXP_PATH = DATASET_FOLDER + os.sep +"InvestmentExperience.csv"
DATA_TXN_PATH = DATASET_FOLDER + os.sep + "Transaction.csv"

df1 = pd.read_csv(DATA_INVEXP_PATH)
df2 = pd.read_csv(DATA_INVEXP_PATH)