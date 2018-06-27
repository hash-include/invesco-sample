from src.main.core import invesco
from src.main.core import myconfig


# Activity table unrolling

def transform_activity_df():
    df = invesco._load_df(myconfig.DATA_ACTIVITY_PATH)
    uniq = sorted(list(map(int, list(df[df.Activity_Type.name].unique()))))
    new_columns = [x for x in uniq]
    for col in new_columns:
        col_name = 'AT' + str(col)
        df[col_name] = df[df.Activity_Count.name][df[df.Activity_Type.name] == str(col)]
        df[col_name] = df[col_name].fillna(0.0).astype(int)

    del df[df.Activity_Type.name]
    del df[df.Activity_Count.name]
    df.to_csv(myconfig.PROCESSED_DATASET_FOLDER + myconfig.SEP + "activity.csv" , date_format=myconfig.DATETIME_FORMAT)

def aum_df():
    col_name = 'aum_per_share'
    aumdf = invesco._load_df(myconfig.DATA_AUM_PATH)
    aumdf[col_name] = -1.0
    for rowidx in range(len(aumdf)):

        row = aumdf.iloc[rowidx]
        a1 = row[aumdf.Shares.name]
        a2 = row[aumdf.AUM.name]
        share_price = a2 / a1 if a1 != 0 else -1.0
        #print(str(a1) + " / " + str(a2) + " / " + str(share_price))
        aumdf.iloc[rowidx , aumdf.columns.get_loc(col_name)] = share_price
    aumdf = aumdf.round(4)
    print(aumdf)
    aumdf.to_csv(myconfig.PROCESSED_DATASET_FOLDER + myconfig.SEP + "AUM.csv", date_format=myconfig.DATETIME_FORMAT)


'''
TODO: 
 We don't know what to do with value= -1 . Let's remove it for now.
'''

if __name__ == '__main__':
    #transform_activity_df()
    aum_df()

