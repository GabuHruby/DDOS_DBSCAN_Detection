import pandas as pd
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score

df = pd.read_csv("RateLimitData.csv")

y_true = df["compromised"].astype(bool)           # actual (attack?)
y_pred = (~df["allowed"].astype(bool))            # predicted attack = blocked

tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
print("TN FP FN TP:", tn, fp, fn, tp)
print("Precision:", precision_score(y_true, y_pred, zero_division=0))
print("Recall:",    recall_score(y_true, y_pred, zero_division=0))
print("F1:",        f1_score(y_true, y_pred, zero_division=0))
print("Accuracy:",  accuracy_score(y_true, y_pred))