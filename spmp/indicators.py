import os
import numpy as np
import pandas as pd

def calc_rsi(stock_data):
    # Calculate the n day RSI
    n = 14

    up_df, down_df = stock_data[['symbol','change_in_price']].copy(), stock_data[['symbol','change_in_price']].copy()

    # For up days, if the change is less than 0 set to 0.
    up_df.loc['change_in_price'] = up_df.loc[(up_df['change_in_price'] < 0), 'change_in_price'] = 0

    # For down days, if the change is greater than 0 set to 0.
    down_df.loc['change_in_price'] = down_df.loc[(down_df['change_in_price'] > 0), 'change_in_price'] = 0

    down_df['change_in_price'] = down_df['change_in_price'].abs()

    # Calculate the EWMA (Exponential Weighted Moving Average), meaning older values are given less weight compared to newer values.
    ewma_up = up_df.groupby('symbol')['change_in_price'].transform(lambda x: x.ewm(span = n).mean())
    ewma_down = down_df.groupby('symbol')['change_in_price'].transform(lambda x: x.ewm(span = n).mean())

    # Calculate the Relative Strength
    relative_strength = ewma_up / ewma_down

    # Calculate the Relative Strength Index
    relative_strength_index = 100.0 - (100.0 / (1.0 + relative_strength))

    stock_data['down_days'] = down_df['change_in_price']
    stock_data['up_days'] = up_df['change_in_price']
    stock_data['RSI'] = relative_strength_index

#Stocastic Oscillator
def stock_osc(stock_data):
    n = 14

    low_14, high_14 = stock_data[['symbol','low']].copy(), stock_data[['symbol','high']].copy()

    # Group by symbol, then apply the rolling function and grab the Min and Max.
    low_14 = low_14.groupby('symbol')['low'].transform(lambda x: x.rolling(window = n).min())
    high_14 = high_14.groupby('symbol')['high'].transform(lambda x: x.rolling(window = n).max())

    # Calculate the Stochastic Oscillator.
    k_percent = 100 * ((stock_data['close'] - low_14) / (high_14 - low_14))

    stock_data['low_14'] = low_14
    stock_data['high_14'] = high_14
    stock_data['k_percent'] = k_percent

#William %R
def william_r(stock_data):
    n = 14

    low_14, high_14 = stock_data[['symbol','low']].copy(), stock_data[['symbol','high']].copy()

    # Group by symbol, then apply the rolling function and grab the Min and Max.
    low_14 = low_14.groupby('symbol')['low'].transform(lambda x: x.rolling(window = n).min())
    high_14 = high_14.groupby('symbol')['high'].transform(lambda x: x.rolling(window = n).max())

    # Calculate William %R indicator.
    r_percent = ((high_14 - stock_data['close']) / (high_14 - low_14)) * - 100

    stock_data['r_percent'] = r_percent

#Moving Average Convergence Divergence
def macd(stock_data):
    ema_26 = stock_data.groupby('symbol')['close'].transform(lambda x: x.ewm(span = 26).mean())
    ema_12 = stock_data.groupby('symbol')['close'].transform(lambda x: x.ewm(span = 12).mean())
    macd = ema_12 - ema_26

    # Calculate the EMA
    ema_9_macd = macd.ewm(span = 9).mean()

    stock_data['MACD'] = macd
    stock_data['MACD_EMA'] = ema_9_macd

# Rate of Price change
def rate_price_change(stock_data):
    n = 9

    # Calculate the Rate of Change in the Price, and store it in the Data Frame.
    stock_data['Price_Rate_Of_Change'] = stock_data.groupby('symbol')['close'].transform(lambda x: x.pct_change(periods = n))


def obv(group):

    # Grab the volume and close column.
    volume = group['volume']
    change = group['close'].diff()

    # intialize the previous OBV
    prev_obv = 0
    obv_values = []

    # calculate the On Balance Volume
    for i, j in zip(change, volume):

        if i > 0:
            current_obv = prev_obv + j
        elif i < 0:
            current_obv = prev_obv - j
        else:
            current_obv = prev_obv

        # OBV.append(current_OBV)
        prev_obv = current_obv
        obv_values.append(current_obv)
    
    return pd.Series(obv_values, index = group.index)

    
