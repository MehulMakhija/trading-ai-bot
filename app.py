import streamlit as st
import yfinance as yf
import pandas as pd
import requests

st.set_page_config(page_title="Real-Time Trading AI", layout="wide")

st.title("📈 Real-Time Trading Signal Bot")

asset_type = st.selectbox("Select Asset Type", ["Stock", "Crypto"])
symbol = st.text_input("Enter Symbol (e.g. AAPL or bitcoin)", value="AAPL" if asset_type == "Stock" else "bitcoin")

def get_stock_data(symbol):
    df = yf.download(symbol, period='2d', interval='1m')
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    return df

def get_crypto_data(symbol):
    url = f'https://api.coingecko.com/api/v3/coins/{symbol}/market_chart?vs_currency=usd&days=1&interval=minutely'
    response = requests.get(url).json()
    prices = [p[1] for p in response['prices']]
    df = pd.DataFrame({'Price': prices})
    df['SMA_20'] = df['Price'].rolling(window=20).mean()
    df['SMA_50'] = df['Price'].rolling(window=50).mean()
    return df

def get_signal(df, price_col):
    latest = df.dropna().iloc[-1]
    if latest['SMA_20'] > latest['SMA_50']:
        return 'BUY', latest[price_col]
    elif latest['SMA_20'] < latest['SMA_50']:
        return 'SELL', latest[price_col]
    else:
        return 'HOLD', latest[price_col]

if symbol:
    if asset_type == "Stock":
        df = get_stock_data(symbol)
        signal, price = get_signal(df, 'Close')
        st.subheader(f"{symbol.upper()} is at ${price:.2f} → **{signal}**")
        st.line_chart(df[['Close', 'SMA_20', 'SMA_50']])
    else:
        df = get_crypto_data(symbol)
        signal, price = get_signal(df, 'Price')
        st.subheader(f"{symbol.upper()} is at ${price:.2f} → **{signal}**")
        st.line_chart(df[['Price', 'SMA_20', 'SMA_50']])
