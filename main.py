import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

def fetch_data(symbol, period="3mo"):
    df = yf.Ticker(symbol).history(period=period)
    df['Daily_Return'] = df['Close'].pct_change() * 100
    df['SMA_10'] = df['Close'].rolling(window=10).mean()
    df['EMA_10'] = df['Close'].ewm(span=10, adjust=False).mean()
    return df

def analyze_stock(symbol):
    df = fetch_data(symbol)
    volatility = np.std(df['Daily_Return'].dropna())

    print(f"Volatility for {symbol}: {volatility:.2f}%")
    df.to_csv(f"data/{symbol}_analysis.csv")

    plt.figure(figsize=(10,5))
    plt.plot(df.index, df['Close'], label='Close Price')
    plt.plot(df.index, df['SMA_10'], label='SMA 10')
    plt.plot(df.index, df['EMA_10'], label='EMA 10')
    plt.legend()
    plt.title(f"{symbol} Price Analysis")
    plt.show()

if __name__ == "__main__":
    analyze_stock("INFY.NS")
