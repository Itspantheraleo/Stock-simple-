import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

def fetch_data(symbol, period="1y"):
    df = yf.Ticker(symbol).history(period=period)
    df['Daily_Return'] = df['Close'].pct_change()
    df['SMA_10'] = df['Close'].rolling(window=10).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    return df

def backtest_sma_strategy(df):
    df = df.copy()
    df['Signal'] = 0
    df.loc[df['SMA_10'] > df['SMA_50'], 'Signal'] = 1  # Buy
    df.loc[df['SMA_10'] < df['SMA_50'], 'Signal'] = -1 # Sell

    df['Strategy_Return'] = df['Signal'].shift(1) * df['Daily_Return']
    cumulative_strategy = (1 + df['Strategy_Return']).cumprod()
    cumulative_buy_hold = (1 + df['Daily_Return']).cumprod()

    return df, cumulative_strategy, cumulative_buy_hold

def plot_results(df, strategy, buy_hold, symbol):
    plt.figure(figsize=(12,6))
    plt.plot(strategy, label='Strategy')
    plt.plot(buy_hold, label='Buy & Hold')
    plt.title(f"Backtest: SMA Crossover - {symbol}")
    plt.legend()
    plt.show()

def run_analysis(symbol):
    df = fetch_data(symbol)
    df, strategy, buy_hold = backtest_sma_strategy(df)
    
    print(f"Final Strategy Return: {strategy.iloc[-1]:.2f}")
    print(f"Final Buy & Hold Return: {buy_hold.iloc[-1]:.2f}")

    df.to_csv(f"data/{symbol}_backtest.csv")
    plot_results(df, strategy, buy_hold, symbol)

if __name__ == "__main__":
    run_analysis("INFY.NS")
