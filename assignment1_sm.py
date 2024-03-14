import statsmodels.api as sm
import pandas as pd
import numpy as np

def to_onehot(col_name:str,data:pd.DataFrame):
    freq = data[col_name].value_counts()
    indx_lst = list(freq.index)
    for idx in indx_lst:
        data[col_name+idx+"_one_hot"] = (data[col_name] == idx).apply(lambda x:int(x))


data = pd.read_csv("data1.csv")
data["y"] = data["Pass"]/data["Total"]
to_onehot("Treat1",data)
to_onehot("Treat2",data)
X_cols = ["Treat1A_one_hot","Treat1B_one_hot","Treat2Y_one_hot","Treat2X_one_hot","Treat2X_one_hot","Dose1","Dose2"]
X = data[X_cols]

link_func_probit = sm.families.links.Probit()
link_func_logit = sm.families.links.Logit()
link_func_loglog = sm.families.links.LogLog()

links = [link_func_probit,link_func_logit,link_func_loglog]
for link in links:
    bin_model = sm.GLM(data["y"],X, family = sm.families.Binomial(link))
    bin_model_results = bin_model.fit()
    print(bin_model_results.summary())