from src.main.core import invesco
from src.main.core import myconfig


tnx = invesco.get_txn_df()
t = tnx.filter(['Unique_Advisor_Id', 'Unique_Investment_Id','Month', 'Transaction_Type', 'Amount'])



