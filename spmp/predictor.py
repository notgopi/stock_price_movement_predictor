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

stock_data = pd.read_csv('stock_data.csv')

stock_data = stock_data[['Symbol','Date','Close','High','Low','Open','Volume']]

#sort the data and calculate the difference of closing prices
#stock_data.sort_values(by = ['symbol','datetime'], inplace = True)

stock_data['Price_Change'] = stock_data['Close'].diff()

#------------- Indicators --------------#



#--------------Train and Test Data-------------#

close_groups = stock_data['Close']

# Apply the lambda function which will return -1.0 for down, 1.0 for up and 0.0 for no change.
close_groups = close_groups.transform(lambda x : np.sign(x.diff()))

# add the data to the main dataframe.
stock_data['Prediction'] = close_groups

# for simplicity in later sections I'm going to make a change to our prediction column. To keep this as a binary classifier I'll change flat days and consider them up days.
stock_data.loc[stock_data['Prediction'] == 0.0] = 1.0

# We need to remove all rows that have an NaN value.
print('Before NaN Drop we have {} rows and {} columns'.format(stock_data.shape[0], stock_data.shape[1]))

# Any row that has a `NaN` value will be dropped.
stock_data = stock_data.dropna()

# Display how much we have left now.
print('After NaN Drop we have {} rows and {} columns'.format(stock_data.shape[0], stock_data.shape[1]))

X_Cols = stock_data[['RSI','k_percent','r_percent','Price_Rate_Of_Change','MACD']]
Y_Cols = stock_data['Prediction']

# Split X and y. KEEP SHUFFLE AS FALSE otherwise it will lead to data leakage
X_train, X_test, y_train, y_test = train_test_split(X_Cols, Y_Cols, random_state=0, shuffle=False, test_size=0.2)

# Create a Random Forest Classifier
rand_frst_clf = RandomForestClassifier(n_estimators = 100, oob_score = True, criterion = "gini", random_state = 0)

# Fit the data to the model
rand_frst_clf.fit(X_train, y_train)

# Make predictions
y_pred = rand_frst_clf.predict(X_test)

print('Correct Prediction (%): ', accuracy_score(y_test, rand_frst_clf.predict(X_test), normalize = True) * 100.0) #Accuracy of predicting the stock price movement after 1 day
