import pandas as pd
import numpy as np
from scipy.special import logit
from scipy.stats import norm
from sklearn.linear_model import LinearRegression, LogisticRegression


def to_onehot(col_name:str,data:pd.DataFrame):
    freq = data[col_name].value_counts()
    indx_lst = list(freq.index)
    for idx in indx_lst:
        data[col_name+idx+"_one_hot"] = (data[col_name] == idx).apply(lambda x:int(x))

def log_log(x:np.ndarray):
    return np.log(-np.log(1-x))


    



data = pd.read_csv("data9.csv")
data["y"] = data["Pass"]/data["Total"]
to_onehot("Treat1",data)
to_onehot("Treat2",data)
data["g_logit"] = data["y"].apply(logit)
data["g_probit"] = data["y"].apply(norm.ppf)
data["g_log_log"] = data["y"].apply(log_log)

logit_reg = LinearRegression()
probit_reg = LinearRegression()
log_log_reg = LinearRegression()


X_cols = ["Treat1A_one_hot","Treat1B_one_hot","Treat2Y_one_hot","Treat2X_one_hot","Treat2X_one_hot","Dose1","Dose2"]
X = data[X_cols]
logit_reg.fit(X,data["g_logit"])
probit_reg.fit(X,data["g_probit"])
log_log_reg.fit(X,data["g_log_log"])

print(logit_reg.score(X,data["g_logit"]))
print(probit_reg.score(X,data["g_probit"]))
print(log_log_reg.score(X,data["g_log_log"]))


logistic_reg = LogisticRegression()
logistic_reg.fit(X,data["y"])
print(logistic_reg.score(X,data["y"]))

# print((data["y"] > 0.7).apply(lambda x:int(x)))
print(data)