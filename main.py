import pandas as pd
import yfinance as yf
import numpy as np

# Download data
data = yf.download("AAPL", start="2015-01-01", end="2024-01-01", progress=False, auto_adjust=True)

if data.empty:
    raise ValueError("Data not loaded")

# Fix columns
data = data.reset_index()
data = data[["Date", "Open", "High", "Low", "Close", "Volume"]]

# Prepare data
x = data[["Open", "High", "Low", "Volume"]].values
y = data["Close"].values.reshape(-1, 1)

# ✅ reshape for LSTM
x = x.reshape((x.shape[0], x.shape[1], 1))

from sklearn.model_selection import train_test_split
xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2, random_state=42)

# Build model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

model = Sequential()
model.add(LSTM(128, return_sequences=True, input_shape=(xtrain.shape[1], 1)))
model.add(LSTM(64))
model.add(Dense(25))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(xtrain, ytrain, batch_size=1, epochs=5)  # reduce epochs first

# Prediction
features = np.array([[177, 180, 177, 74919600]])
features = features.reshape((1, 4, 1))

y_pred = model.predict(features)
print(y_pred)

import plotly.graph_objects as go

fig = go.Figure()

fig.add_trace(go.Scatter(y=ytest.flatten(), mode='lines', name='Actual'))
fig.add_trace(go.Scatter(y=y_pred.flatten(), mode='lines', name='Predicted'))

fig.update_layout(title="Stock Prediction",
                  xaxis_title="Time",
                  yaxis_title="Price")

fig.show()
