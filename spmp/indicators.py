import os
import numpy as np
import pandas as pd

def calc_rsi(stock_data):
    n = 14 # Calculate the 14 day RSI
    
    # First make a copy of the data frame twice
    up_df, down_df = stock_data[['Symbol','Price_Change']].copy(), stock_data[['Symbol','Price_Change']].copy()
    up_df.loc['Price_Change'] = up_df.loc[(up_df['Price_Change'] < 0), 'Price_Change'] = 0
    
    down_df.loc['Price_Change'] = down_df.loc[(down_df['Price_Change'] > 0), 'Price_Change'] = 0
    down_df['Price_Change'] = down_df['Price_Change'].abs()
    
    # Calculate the EWMA (Exponential Weighted Moving Average), meaning older values are given less weight compared to newer values.
    ewma_up = up_df.groupby('Symbol')['Price_Change'].transform(lambda x: x.ewm(span = n).mean())
    ewma_down = down_df.groupby('Symbol')['Price_Change'].transform(lambda x: x.ewm(span = n).mean())
    
    # Calculate the Relative Strength
    relative_strength = ewma_up / ewma_down
    
    # Calculate the Relative Strength Index
    relative_strength_index = 100.0 - (100.0 / (1.0 + relative_strength))

    return down_df['Price_Change'], up_df['Price_Change'], relative_strength_index

#Stocastic Oscillator
def stock_osc(stock_data):
    n = 14

    low_14, high_14 = stock_data[['Symbol','Low']].copy(), stock_data[['Symbol','High']].copy()

    # Group by symbol, then apply the rolling function and grab the Min and Max.
    low_14 = low_14.groupby('Symbol')['Low'].transform(lambda x: x.rolling(window = n).min())
    high_14 = high_14.groupby('Symbol')['High'].transform(lambda x: x.rolling(window = n).max())

    # Calculate the Stochastic Oscillator.
    k_percent = 100 * ((stock_data['Close'] - low_14) / (high_14 - low_14))

    return low_14, high_14, k_percent

#William %R
def william_r(stock_data):
    n = 14

    low_14, high_14 = stock_data[['Symbol','Low']].copy(), stock_data[['Symbol','High']].copy()

    # Group by symbol, then apply the rolling function and grab the Min and Max.
    low_14 = low_14.groupby('Symbol')['Low'].transform(lambda x: x.rolling(window = n).min())
    high_14 = high_14.groupby('Symbol')['High'].transform(lambda x: x.rolling(window = n).max())

    # Calculate William %R indicator.
    r_percent = ((high_14 - stock_data['Close']) / (high_14 - low_14)) * - 100

    return r_percent

#Moving Average Convergence Divergence
def macd(stock_data):
    ema_26 = stock_data.groupby('Symbol')['Close'].transform(lambda x: x.ewm(span = 26).mean())
    ema_12 = stock_data.groupby('Symbol')['Close'].transform(lambda x: x.ewm(span = 12).mean())
    macd = ema_12 - ema_26

    ema_9_macd = macd.ewm(span = 9).mean()

    return macd, ema_9_macd

# Rate of Price change
def rate_price_change(stock_data):
    n = 9

    df = stock_data.groupby('Symbol')['Close'].transform(lambda x: x.pct_change(periods = n))
    return df

#On Balance Volume
def obv(group):
    volume = group['Volume']
    change = group['Close'].diff()

    prev_obv = 0
    obv_values = []

    for i, j in zip(change, volume):

        if i > 0:
            current_obv = prev_obv + j
        elif i < 0:
            current_obv = prev_obv - j
        else:
            current_obv = prev_obv

        prev_obv = current_obv
        obv_values.append(current_obv)
    
    return pd.Series(obv_values, index = group.index)
