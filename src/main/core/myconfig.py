import os

current_dir = os.path.realpath(__file__)
RESOURCE_FOLDER = os.sep.join(current_dir.split(os.sep)[:-2]) + os.sep + "resources"
DATASET_FOLDER = RESOURCE_FOLDER + os.sep + "dataset"
PROCESSED_DATASET_FOLDER = RESOURCE_FOLDER + os.sep + "processed_dataset"
DATA_ACTIVITY_PATH = DATASET_FOLDER + os.sep + "Activity.csv"
DATA_AUM_PATH = DATASET_FOLDER + os.sep + "AUM.csv"
DATA_INVEXP_PATH = DATASET_FOLDER + os.sep +"InvestmentExperience.csv"
DATA_TXN_PATH = DATASET_FOLDER + os.sep + "Transaction.csv"
DATA_TEST_PATH = DATASET_FOLDER + os.sep + "test_data.csv"

DATETIME_FORMAT = '%Y / %m'

SEP = os.sep

if __name__ == '__main__':

    print(DATASET_FOLDER)
    print(RESOURCE_FOLDER)
