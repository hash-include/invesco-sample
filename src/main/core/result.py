'''
Generate aid, iid, actual_txn, propensity_score, predicted_txn
'''

from src.main.core import invesco
from src.main.core import myconfig
from src.main.core.algorithms import cf1
import numpy as np
import pprint


class Validation(object):
    def __init__(self, month):
        self.month = month
        self.__load()

    def __load(self):
        self.cf = cf1.CF1(month=self.month)

        self.vset = invesco.get_txn_df()
        if month:
            self.vset = self.vset[self.vset.Month > invesco.get_datetime(self.month)]

        self.nrows = len(self.vset)

    def get_validation_set(self):
        print("# Rows in vset: " + str(self.nrows))
        self.vset['Propensity_Score'] = 0.0

        for rowidx in range(self.nrows):
            row = self.vset.iloc[rowidx]
            aid = row['Unique_Advisor_Id']
            iid = row['Unique_Investment_Id']
            propensity_score = self.cf.get_value(aid, iid)
            self.vset.iloc[rowidx, self.vset.columns.get_loc('Propensity_Score')] = propensity_score
        return self.vset

    def tune_threshold(self, thres_start=0.1, thres_step=0.1, thres_end=1.0):
        thresholds = np.linspace(0.0, 1.0, 20)
        acc_dict = {}
        for threshold in thresholds:
            acc_dict[str(threshold)] = self.get_accuracy(threshold)
        return acc_dict

    def get_accuracy(self, threshold):
        '''
        if Score > Threshold, then advisor will redeem the investment
            Then Redeem_Status field need to store YES
        otherwise:
        
        :param threshold: 
        :return: 
        '''
        correct = 0
        for rowidx in range(self.nrows):
            row = self.vset.iloc[rowidx]
            propensity_score = self.vset.iloc[rowidx, self.vset.columns.get_loc('Propensity_Score')]
            actual = row['Transaction_Type']
            prediction = 'R' if propensity_score > threshold else 'P'
            # if propensity_score > threshold and actual == 'R':
            #     correct += 1
            if actual == prediction:
                correct += 1

        return float(correct / self.nrows) * 100

    def predict(self, threshold, default_prediction='NO'):
        '''
        Fields:
            Provided:
                Unique_Advisor_Id
                Unique_Investment_Id
            Compute:
                Propensity_Score
                Redeem_Status                                
            
        :param filepath: 
        :return: 
        '''
        test_df = invesco.get_test_df()
        test_df['Propensity_Score'] = 0.0
        test_df['Redeem_Status'] = default_prediction

        for rowidx in range(len(test_df)):
            aid = test_df.iloc[rowidx, test_df.columns.get_loc('Unique_Advisor_Id')]
            iid = test_df.iloc[rowidx, test_df.columns.get_loc('Unique_Investment_Id')]

            score = self.cf.get_value(aid, iid)
            test_df.iloc[rowidx, test_df.columns.get_loc('Propensity_Score')] = score
            if score > threshold:
                test_df.iloc[rowidx, test_df.columns.get_loc('Redeem_Status')] = 'YES'
        return test_df


if __name__ == '__main__':
    month = '2016 / 12'
    v = Validation(month)
    v.get_validation_set()
    pprint.pprint(v.tune_threshold())
    output_path = myconfig.PROCESSED_DATASET_FOLDER + myconfig.SEP + "output3.csv"
    out_df = v.predict(0.6)
    header = ['Unique_Advisor_Id', 'Unique_Investment_Id', 'Propensity_Score', 'Redeem_Status']
    out_df.to_csv(output_path, float_format='%.5f')
    print("Done")
