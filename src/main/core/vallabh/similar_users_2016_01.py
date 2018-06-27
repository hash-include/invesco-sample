#importing pandas
import pandas as pd

#storing file in filename
filename = 'similarusers_2016-01.csv'

#storing the flatfile in a pandas dataframe
df = pd.read_csv(filename)

#storing the required attributes Unique_Advisor_Id and Unique_Investment_Id into a different dataframe
df1 = df[['Unique_Advisor_Id' , 'Unique_Investment_Id']]


#this counts the number of times an investor invests in a particular investment id
print(df1.groupby(df1.columns.tolist(),as_index=False).size())

df2 = df1.groupby(df1.columns.tolist(),as_index=False).size()

df2.groupby('Unique_Advisor_Id')['size'].apply(' '.join).reset_index()