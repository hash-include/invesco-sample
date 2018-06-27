'''
1. Create a feature vector given advisor id, investment id and month. 
2. Class label will be P/R for give aid, iid and month from txn table.

feature vector:
- Activity features of aid of M-1.
- Inv experience of iid of M-1.
- AUM of aid, iid for M-1.
- TXN for aid, iid for M 
    - Considering only TXN_TYPE P/R for now. Ignoring code_* and Amount feature.
    
todo:
1. Convert AT* values to integer instead of float in activity dataframe.
'''
import pandas as pd

from src.main.core import invesco
from src.main.core import myconfig

start_month = '2016 / 02'
end_month = '2016 / 12'

tnx = invesco.get_txn_df()
activity = invesco.get_activity_df()
aum = invesco.get_aum_df()
invexp = invesco.get_invexp_df()  # What to do with empty cells? - 10 Yr projection?

data = pd.merge(aum, activity, how='left', on=['Unique_Advisor_Id', 'Month']).fillna(0.0)
print("Level 1 Merge: " + str(len(data)))
data = pd.merge(data, invexp, how='left', on=['Unique_Investment_Id', 'Month']).fillna(0.0)
print("Level 2 Merge: " + str(len(data)))
print(data.head(10))

data['class_label'] = 'X'

print("Length of dataset: " + str(len(data)))
for rowidx in range(len(data)):
    class_label = None
    this_month = data.get_value(rowidx, 'Month')
    next_month = invesco.get_next_month(this_month)

    this_aid = data.get_value(rowidx, 'Unique_Advisor_Id')
    this_iid = data.get_value(rowidx, 'Unique_Investment_Id')

    t3 = tnx[
        (tnx.Unique_Advisor_Id == this_aid)
        & (tnx.Unique_Investment_Id == this_iid)
        & (tnx.Month == next_month)
        ]

    if len(t3) == 0:
        # class_label = 'H'
        class_label = 0.0
    else:
        p_amount = 0.0
        r_amount = 0.0
        for t3idx in range(len(t3)):
            txn_type = t3.iloc[t3idx, t3.columns.get_loc('Transaction_Type')]
            amt_str = t3.iloc[t3idx, t3.columns.get_loc('Amount')]
            # print("AID : %s / IID: %s / Row Idx: %s  / Amount: %s" % (this_aid, this_iid, rowidx, amt_str))
            amount = abs(float(amt_str))
            if txn_type == 'P':
                p_amount = amount
            else:
                r_amount = amount
        if r_amount > p_amount:
            # class_label = 'R'
            class_label = 1.0
        else:
            class_label = 0.0
    data.iloc[rowidx, data.columns.get_loc('class_label')] = class_label

    if rowidx % 1000 == 0:
        print("Row: " + str(rowidx))

data.to_csv(myconfig.PROCESSED_DATASET_FOLDER + myconfig.SEP + "dataset.csv")
