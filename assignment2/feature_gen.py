import pandas as pd
import datetime as dt
import csv

file = open("features.csv","w")
writer = csv.writer(file)

xls = pd.ExcelFile("Assignment2-201801-202210.xlsx")
transactions_df = pd.read_excel(xls,0)
churn_df = pd.read_excel(xls,1)

# Time since last transaction, size of last trans, cost of last trans, avg freq of trans before last transac, cost of trans per unit time, size of trans per unit time


def to_days_from_end(date,f = dt.date(2022,10,31)):
    d = date.date()
    t = f-d
    return t.days

def to_months_from_end(date,f = dt.date(2022,10,31)):
    d = date.date()
    m_d = d.month
    y_d = d.year
    m_f = f.month
    y_f = f.year
    return m_f - m_d + (y_f - y_d)*12 

def find_churn_stat(cust_id:str):
    row_df = churn_df[churn_df["CustomerID"] == cust_id]
    if not row_df.empty:
        return 1
    else:
        return 0

def get_cust_rows(cust_id:str):
    return transactions_df[transactions_df["CustomerID"] == cust_id]

def convert_to_months_from_end():
    d = transactions_df["TransMonth"]
    for i,rows in transactions_df.iterrows():
        transactions_df.loc[i,"TransMonth"] = to_months_from_end(d[i])
    
def find_features(cust_id):
    rows = get_cust_rows(cust_id)
    last_trans = min(rows["TransMonth"])
    first_trans = max(rows["TransMonth"])
    no_of_trans = len(rows)
    time_period = first_trans-last_trans+1
    trans_per_unit_time = no_of_trans/time_period
    cost_last_trans = int(rows[rows["TransMonth"] == last_trans]["MonthlySaleValueLocal"])
    size_last_trans = int(rows[rows["TransMonth"] == last_trans]["MonthlyQuantitySold"])
    total_cost = sum(rows["MonthlyQuantitySold"])
    cost_per_unit_time = total_cost/time_period
    cost_per_trans = total_cost/no_of_trans
    total_size = sum(rows["MonthlySaleValueLocal"])
    size_per_unit_time = total_size/time_period
    size_per_trans = total_size/no_of_trans
    churn = find_churn_stat(cust_id)
    features = [cust_id,last_trans,first_trans,cost_last_trans,size_last_trans,no_of_trans,time_period,trans_per_unit_time,no_of_trans,cost_per_unit_time,cost_per_trans,total_cost,size_per_unit_time,size_per_trans,churn]
    return features

def clean_data():
    problem = transactions_df[transactions_df["MonthlyQuantitySold"] == "#NUM!"]
    transactions_df.drop(problem.index,inplace=True)


feature_names = ["CustomerID","LastTrans","FirstTrans","LastTransCost","SizeLastTrans","NoTrans","TimePeriod","TransPerUnitTime","NoOfTrans","CostPerUnitTime","CostPerTrans","TotalCost","SizePerUnitTime","SizePerTrans","Churn"]
writer.writerow(feature_names)
convert_to_months_from_end()
clean_data()
done = []
for i,rows in transactions_df.iterrows():
    cust_id = transactions_df["CustomerID"][i]
    if cust_id in done:
        continue
    features = find_features(cust_id)
    writer.writerow(features)
    done.append(cust_id)



# for i in range(len(d)):
#     transactions_df.loc[i,"TransMonth"] = to_days_from_end(d[i]) 


# f = dt.date(2022,10,31)
# t = f-d
# print(type(t.days))
# print(type(d))
# print(churn_df)

# clean_data()
# S = 0
# for i,rows in transactions_df.iterrows():
#     try:
#         S += transactions_df["MonthlyQuantitySold"][i]
#     except:
#         print(transactions_df["MonthlyQuantitySold"][i],transactions_df["CustomerID"][i])
# print(S)

# cust_id = transactions_df["CustomerID"][0]
# clean_data()
# convert_to_months_from_end()
# features = find_features(cust_id)
# print(features)