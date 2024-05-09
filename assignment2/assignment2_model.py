import statsmodels.api as sm
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, confusion_matrix, roc_auc_score,precision_recall_fscore_support, ConfusionMatrixDisplay
from matplotlib import pyplot as  plt


features_data = pd.read_csv("features.csv")

X_cols = ["LastTrans","FirstTrans","LastTransCost","SizeLastTrans","TimePeriod","TransPerUnitTime","NoOfTrans","CostPerUnitTime","CostPerTrans","TotalCost","SizePerUnitTime","SizePerTrans"]
train_data, test_data = train_test_split(features_data,test_size = 0.2,random_state=0) 
train_y = train_data["Churn"]
train_x = train_data[X_cols]
test_x = test_data[X_cols]
test_y = test_data["Churn"]

link = sm.families.links.Logit()
logit_model = sm.GLM(train_y,train_x,family=sm.families.Binomial(link))
logit_model_results = logit_model.fit()
print(logit_model_results.summary())

# y_pred = logit_model_results.predict(test_x)
# y_pred_bin = (y_pred > 0.5).astype(int)
# correct = sum((y_pred_bin == test_y).astype(int))
# n = len(y_pred)
# acc = correct/n
# print(acc)

def accuracy(model_results,test_x:pd.DataFrame,test_y:pd.DataFrame,cut_off:float = 0.5):
    y_pred = model_results.predict(test_x)
    y_pred_bin = (y_pred > cut_off).astype(int)
    correct = sum((y_pred_bin == test_y).astype(int))
    n = len(y_pred)
    acc = correct/n
    return acc

def confusion(model_results, test_x:pd.DataFrame,test_y:pd.DataFrame,cut_off = 0.5):
    y_pred = model_results.predict(test_x)
    y_pred_bin = (y_pred > cut_off).astype(int)
    m = confusion_matrix(test_y,y_pred_bin)
    m[0] = m[0]*100/sum(m[0])
    m[1] = m[1]*100/sum(m[1]) 
    disp = ConfusionMatrixDisplay(confusion_matrix=m)
    disp.plot()
    plt.show()
    return m

train_acc = accuracy(logit_model_results,train_x,train_y)
test_acc = accuracy(logit_model_results,test_x,test_y)
print("Training set Accuracy: ",train_acc*100,"%")
print("Testing Set Accuracy:",test_acc*100,"%")
m = confusion(logit_model_results,test_x,test_y)
print("Confusion Matrix:\n",m)
