import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import plot_roc_curve
from sklearn.metrics import accuracy_score, classification_report

import indicators

stock_data = pd.read_csv('stock_price.csv')
stock_data.head()

stock_data = stock_data[['Symbol','Date','Close','High','Low','Open','Volume']]

#sort the data and calculate the difference of closing prices
stock_data.sort_values(by = ['symbol','datetime'], inplace = True)
stock_data['price_change'] = stock_data['close'].diff()

# apply the function to each group
obv_groups = stock_data.groupby('symbol').apply(indicators.obv)

# add to the data frame, but drop the old index, before adding it.
stock_data['On Balance Volume'] = obv_groups.reset_index(level=0, drop=True)

# display the data frame.
stock_data.head(30)
