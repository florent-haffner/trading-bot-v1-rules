# Make sure that you have all these libaries available to run the code successfully
import datetime as dt
import urllib.request, json
import os

from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd

import numpy as np
import tensorflow as tf  # This code has been tested with TensorFlow 1.6
from sklearn.preprocessing import MinMaxScaler

from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_STOCK')
df = None


#
# https://www.datacamp.com/community/tutorials/lstm-python-stock-market
#


def getTextFile(path):
    global df
    df = pd.read_csv(path, delimiter="\t")


def queryDatasAndParseCSV(ticker):
    global df
    url_string = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&outputsize=full&apikey=%s" % (
        ticker, api_key)
    file_to_save = 'stock_market_data-%s.csv' % ticker

    if not os.path.exists(file_to_save):
        with urllib.request.urlopen(url_string) as url:
            data = json.loads(url.read().decode())
            # extract stock market data
            data = data['Time Series (Daily)']
            df = pd.DataFrame(columns=['Date', 'Low', 'High', 'Close', 'Open'])
            for k, v in data.items():
                date = dt.datetime.strptime(k, '%Y-%m-%d')
                data_row = [date.date(), float(v['3. low']), float(v['2. high']),
                            float(v['4. close']), float(v['1. open'])]
                df.loc[-1, :] = data_row
                df.index = df.index + 1
        print('Data saved to : %s' % file_to_save)
        df.to_csv(file_to_save)

    else:
        print('File already exists. Loading data from CSV')
        df = pd.read_csv(file_to_save)


# pathToFile = "hpq.us.txt"
# getTextFile(pathToFile)

# stockName = "AAL"
stockName = "IBM"
queryDatasAndParseCSV(stockName)

# Sort DataFrame by date
df = df.sort_values('Date')

plt.figure(figsize=(18, 9))
plt.plot(range(df.shape[0]), (df['Low'] + df['High']) / 2.0)
plt.xticks(range(0, df.shape[0], 500), df['Date'].loc[::500], rotation=45)
plt.xlabel('Date', fontsize=18)
plt.ylabel('Mid Price', fontsize=18)
plt.show()

# First calculate the mid prices from the highest and lowest
high_prices = df.loc[:, 'High'].to_numpy()
low_prices = df.loc[:, 'Low'].to_numpy()
mid_prices = (high_prices + low_prices) / 2.0

dataset_size = len(mid_prices)
train_size = int(dataset_size * 0.8)
test_size = int(dataset_size * 0.2)

print(dataset_size, train_size, test_size)

# Split train and test sets
train_data = mid_prices[:train_size]
test_data = mid_prices[test_size:]

# dataset_size = len(mid_prices)
# train_size = int(dataset_size * 0.8)
# test_size = int(dataset_size * 0.2)
#
# # Split train and test sets
# train_data = mid_prices[:train_size]
# test_data = mid_prices[test_size:]


# Scale the data to be between 0 and 1
# When scaling remember! You normalize both test and train data with respect to training data
# Because you are not supposed to have access to test data
scaler = MinMaxScaler()
train_data = train_data.reshape(-1, 1)
test_data = test_data.reshape(-1, 1)

print('train_data', len(train_data))
print('test_data', len(test_data))

# Train the Scaler with training data and smooth data
smoothing_window_size = 1000
for di in range(0, dataset_size, smoothing_window_size):
    try:
        scaler.fit(train_data[di:di + smoothing_window_size])
        train_data[di:di + smoothing_window_size] = scaler.transform(train_data[di:di + smoothing_window_size])
    except ValueError:
        pass

    # # You normalize the last bit of remaining data
    # scaler.fit(train_data[di + smoothing_window_size:])
    # train_data[di + smoothing_window_size:] = scaler.transform(train_data[di + smoothing_window_size:])

    # Reshape both train and test data
    # train_data = train_data.reshape(-1)
    # test_data = scaler.transform(test_data).reshape(-1)

# Normalize test data
plt.plot(test_data)
plt.title('not scaled bro')
plt.show()

# Now perform exponential moving average smoothing
# So the data will have a smoother curve than the original ragged data
EMA = 0.0
gamma = 0.1
for ti in range(dataset_size - 2000): # Used 11'000 at first but we use significantly less data so...
    EMA = gamma * train_data[ti] + (1 - gamma) * EMA
    train_data[ti] = EMA

# Used for visualization and test purposes
all_mid_data = np.concatenate([train_data, test_data], axis=0)

#
# One-Step Ahead Prediction via Averaging
#
