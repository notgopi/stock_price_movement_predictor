import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import plot_roc_curve
from sklearn.metrics import accuracy_score, classification_report

price_data = pd.read_csv('price_data.csv')
price_data.head()

price_data = price_data[['symbol','datetime','close','high','low','open','volume']]

#sort the data
price_data.sort_values(by = ['symbol','datetime'], inplace = True)
price_data['price_change'] = price_data['close'].diff()