"""
Apply Collaborative filtering 
    - Try both item - item based and user - user based approach.
"""
from src.main.core import invesco
from src.main.core import myconfig
import pandas as pd

__EPSILON = 1e-9


def compute_cfmat(month=None):
    df = invesco.get_txn_df()
    if month:
        df = df[df.Month <= invesco.get_datetime(month)]

    print("#Rows: " + str(len(df)))
    x = pd.DataFrame(df, columns=[df.Unique_Advisor_Id.name, df.Unique_Investment_Id.name, df.Transaction_Type.name])
    x['count'] = 0

    y = x.groupby([x.Unique_Advisor_Id.name, x.Unique_Investment_Id.name, x.Transaction_Type]).count().reset_index()

    pcounts = y[y.Transaction_Type == 'P']
    rcounts = y[y.Transaction_Type == 'R']

    pmat = pd.DataFrame(pcounts, columns=[pcounts.Unique_Advisor_Id.name, pcounts.Unique_Investment_Id.name, 'count'])
    rmat = pd.DataFrame(rcounts, columns=[rcounts.Unique_Advisor_Id.name, rcounts.Unique_Investment_Id.name, 'count'])

    users = set()
    items = set()

    users = users.union(set(pmat[pmat.Unique_Advisor_Id.name].unique()))
    users = users.union(set(rmat[rmat.Unique_Advisor_Id.name].unique()))

    items = items.union(set(pmat[pmat.Unique_Investment_Id.name].unique()))
    items = items.union(set(rmat[rmat.Unique_Investment_Id.name].unique()))

    print("USERS: \n")
    print(users)

    print("\nITEMS")
    print(items)

    columns = list(sorted(list(items)))
    rows = list(sorted(list(users)))

    cfmat = pd.DataFrame(index=rows, columns=columns).fillna(0)

    for user in users:
        for item in items:
            pvalc = 0.0
            rvalc = 0.0

            rval = rmat[rmat.Unique_Advisor_Id == user]
            rval = rval[rval.Unique_Investment_Id == item]
            if (len(rval) > 0):
                rvalc = float(rval['count'])

            pval = pmat[pmat.Unique_Advisor_Id == user]
            pval = pval[pval.Unique_Investment_Id == item]
            if (len(pval) > 0):
                pvalc = float(pval['count'])

            prob = float(rvalc / (__EPSILON + rvalc + pvalc))
            # print("user : " + user + " / item: " + item + " / pvalc : " + str(pvalc) + " / rvalc : " + str(rvalc) + " / prob: " + str(prob))
            cfmat.loc[user, item] = prob
    return cfmat


if __name__ == '__main__':
    cfmat = compute_cfmat(month='2016 / 10')
    # pmat.to_csv(myconfig.PROCESSED_DATASET_FOLDER + myconfig.SEP + "purchase_mat.csv")
    # rmat.to_csv(myconfig.PROCESSED_DATASET_FOLDER + myconfig.SEP + "redeem_mat.csv")
    cfmat.to_csv(myconfig.PROCESSED_DATASET_FOLDER + myconfig.SEP + "cfmat.csv")
    print("Done")
