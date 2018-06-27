import pandas as pd
import os
from src.main.core import myconfig
from datetime import datetime

# All fields other than these are treated as int64.
# Need to convert 'Month' to date explicitly.
__dtypedict = {
    'Unique_Advisor_Id': 'str',
    'Unique_Investment_Id': 'str',
    'Activity_Type': 'str',
    # INVEXP fields
    'Morningstar_Category': 'str',
    'Investment': 'str',
    # Txn fields
    'Code_1': 'str',
    'Code_2': 'str',
    'Code_3': 'str',
    'Code_4': 'str',
    'Code_5': 'str'
}

__datetime_dtype = ['Month']

# pd.options.display.float_format = '{:,.4f}'.format

__dfmap = dict()

KEY_AID = 'Unique_Advisor_Id'
KEY_IID = 'Unique_Investment_Id'
KEY_MONTH = 'Month'

KEY_TXN_TYPE = 'Transaction_Type'
KEY_TXN_Code_1 = 'Code_1'
KEY_TXN_Code_2 = 'Code_2'
KEY_TXN_Code_3 = 'Code_3'
KEY_TXN_Code_4 = 'Code_4'
KEY_TXN_Code_5 = 'Code_5'
KEY_TXN_Amount = 'Amount'

KEY_AUM_Shares = 'Shares'
KEY_AUM_Value = 'AUM'

# To be computed
KEY_AUM_Price = 'Share_Price'

KEY_INVEXP_Morningstar_Category = 'Morningstar Category'
KEY_INVEXP_Investment = 'Investment'
KEY_INVEXP_Rating = 'Rating'
KEY_INVEXP_1_Yr_Rank = '1 Yr % Rank'
KEY_INVEXP_3_Yr_Rank = '3 Yr % Rank'
KEY_INVEXP_5_Yr_Rank = '5 Yr % Rank'
KEY_INVEXP_10_Yr_Rank = '10 Yr % Rank'
KEY_INVEXP_1_Yr_Return = '1 Yr Return'
KEY_INVEXP_3_Yr_Return = '3 Yr Return'
KEY_INVEXP_5_Yr_Return = '5 Yr Return'
KEY_INVEXP_10_Yr_Return = '10 Yr Return'
KEY_INVEXP_1_Yr_Excess_Return_vs_Primary_Ix = '1 Yr Excess Return vs Primary Ix'
KEY_INVEXP_3_Yr_Excess_Return_vs_Primary_Ix = '3 Yr Excess Return vs Primary Ix'
KEY_INVEXP_5_Yr_Excess_Return_vs_Primary_Ix = '5 Yr Excess Return vs Primary Ix'
KEY_INVEXP_10_Yr_Excess_Return_vs_Primary_Ix = '10 Yr Excess Return vs Primary Ix'
KEY_INVEXP_1_Yr_Excess_Return_vs_Category_Ix = '1 Yr Excess Return vs Category Ix'
KEY_INVEXP_3_Yr_Excess_Return_vs_Category_Ix = '3 Yr Excess Return vs Category Ix'
KEY_INVEXP_5_Yr_Excess_Return_vs_Category_Ix = '5 Yr Excess Return vs Category Ix'
KEY_INVEXP_10_Yr_Excess_Return_vs_Category_Ix = '10 Yr Excess Return vs Category Ix'
KEY_INVEXP_Net_Flows = 'Net Flows'


def _load_df(filepath):
    x = pd.read_csv(filepath, dtype=__dtypedict, nrows=10000)
    # x = pd.read_csv(filepath, dtype=__dtypedict)
    for field in __datetime_dtype:
        if field in x:
            x[field] = pd.to_datetime(x[field])
    return x


def __get_frame(filepath, cached=True):
    if cached and filepath in __dfmap:
        return __dfmap[filepath]
    x = _load_df(filepath)
    __dfmap[filepath] = x
    return x


def get_activity_df():
    '''
    Flatten the activity type and activity count values.
    :return: 
    '''
    df = __get_frame(myconfig.DATA_ACTIVITY_PATH).copy(deep=True)
    uniq = sorted(list(map(int, list(df[df.Activity_Type.name].unique()))))
    new_columns = [x for x in uniq]
    for col in new_columns:
        col_name = 'AT' + str(col)
        df[col_name] = df[df.Activity_Count.name][df[df.Activity_Type.name] == str(col)]
        df[col_name] = df[col_name].fillna(0.0).astype(int)

    del df[df.Activity_Type.name]
    del df[df.Activity_Count.name]
    return df


def get_aum_df():
    df = __get_frame(myconfig.DATA_AUM_PATH).copy(deep=True)

    return __get_frame(myconfig.DATA_AUM_PATH).copy(deep=True)


def get_txn_df():
    raw_frame = __get_frame(myconfig.DATA_TXN_PATH)
    return raw_frame.copy(deep=True)


def get_invexp_df():
    return __get_frame(myconfig.DATA_INVEXP_PATH).copy(deep=True)


def get_test_df():
    return __get_frame(myconfig.DATA_TEST_PATH).copy(deep=True)


def get_summary(df):
    summary = ''
    for column in df.columns:
        desc = df[column].describe()
        summary += "\n".join(str(desc).split("\n"))
        summary += '\n\n'
    return summary


def write_stats(write=False, filename=None):
    if write:
        fname = myconfig.RESOURCE_FOLDER + os.sep + 'stats.txt'
        if filename:
            fname = filename

        with open(fname, 'w') as f:
            f.write("--- START ---\n")
            f.write("\n--- ACTIVITY ---\n")
            f.write(get_summary(get_activity_df()))
            f.write("\n--- AUM ---\n")
            f.write(get_summary(get_aum_df()))
            f.write("\n--- INVEXP ---\n")
            f.write(get_summary(get_invexp_df()))
            f.write("\n--- TXN ---\n")
            f.write(get_summary(get_txn_df()))
            f.write("\n--- END ---")


def get_datetime(month):
    return datetime.strptime(month, myconfig.DATETIME_FORMAT)


def get_last_month(d):
    # # http://stackoverflow.com/questions/4130922/how-to-increment-datetime-by-custom-months-in-python-without-using-library
    last_month = datetime(int(d.year - (d.month / 12)), (((d.month - 1) % 12) + 1), 1)
    return last_month


def get_next_month(d):
    # # http://stackoverflow.com/questions/4130922/how-to-increment-datetime-by-custom-months-in-python-without-using-library
    next_month = datetime(int(d.year + (d.month / 12)), ((d.month % 12) + 1), 1)
    return next_month


if __name__ == '__main__':
    # write_stats(write=True)
    pass
