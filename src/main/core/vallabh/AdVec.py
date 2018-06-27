from src.main.core import invesco

txn_df = invesco.get_txn_df()

aum_df = invesco.get_aum_df()


def get_p_txns(uaid, month = None):
    '''
    1. Get all transactions made by this user
    2. Filter out only P transactions
    
    Later:
    To consider month parameter also.     
    :param uaid: 
    :return: 
    '''
    txns = txn_df[txn_df.Unique_Advisor_Id == uaid]
    if month:
        if isinstance(month, str):
            invesco.get_datetime(month)
        txns = txns[txn_df.Month <= month]

    ptxns = txns[txn_df.Transaction_Type == 'P']
    rtxns = txns[txn_df.Transaction_Type == 'R']
    ptxn_count = len(ptxns)
    rtxn_count = len(rtxns)
    total_txns = len(txns)
    total_p_amount = ptxns[txn_df.Amount.name].sum()
    total_r_amount = rtxns[txn_df.Amount.name].sum()
    return ptxn_count, rtxn_count, total_txns, total_p_amount, total_r_amount



def get_aum(uaid , month = None):
    '''
    1. Get AUM of this user when he does P Transactions
    2. Get AUM of this user when he does R Transactions
    
    Later:
    3. Use month parameter also
    
    
    :param uaid: 
    :param month: 
    :return: 
    '''

    aum_p_tnx = 0
    aum_r_tnx = 0
    aum_total_tnx = 0

    aum = aum_df[aum_df.Unique_Advisor_Id == uaid]
    temp = txn_df[txn_df.Unique_Advisor_Id == uaid]
    temp1 = temp[temp.Transaction_Type == 'P']
    invids = set(temp1.Unique_Investment_Id)
    ptrnx_aum_sum = 0
    for invid in invids:
        aum2 = aum[aum.Unique_Investment_Id == invid ]
        ptrnx_aum_sum = ptrnx_aum_sum + aum2[aum2.AUM.name].sum()

    aum_for_p = aum[ptnx.Unique_Investment_Id == aum.Unique_Advisor_Id]

    aum_total_tnx = aum[aum_df.AUM.name].sum()




def get_advisor_vector(uaid):
    '''
    1. Number of P transactions w/o month 
    
    :param uaid: 
    :return: 
    '''
    F_P_TXNS_COUNT = get_p_txns(uaid)

    return []

# Test code
uaid = '1000103'
month = '2016 / 01'

if __name__ == '__main__':
    print("")



