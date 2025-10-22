
import yfinance as yf
import pandas as pd

# Financial sector tickers
TICKERS = [
    "HDFCBANK.NS","ICICIBANK.NS","AXISBANK.NS","KOTAKBANK.NS","SBIN.NS",
    "BAJFINANCE.NS","BAJAJFINSV.NS","HDFCLIFE.NS","ICICIPRULI.NS",
    "LICHSGFIN.NS","MUTHOOTFIN.NS","PNB.NS","BANKBARODA.NS","IDFCFIRSTB.NS",
    "FEDERALBNK.NS","RBLBANK.NS","YESBANK.NS","SHRIRAMFIN.NS","REC.NS",
    "PFC.NS","ICICIGI.NS","HDFCAMC.NS","BAJAJHLDNG.NS"
]

def calculate_returns(period="1d"):
    """
    period: '1d', '7d', '30d'
    Returns a dict with top 10 gainers and losers
    """
    data = yf.download(TICKERS, period="2mo", interval="1d", group_by='ticker', progress=False)
    returns = {}

    for ticker in TICKERS:
        try:
            df = data[ticker].get('Adj Close', data[ticker].get('Close')).dropna()
            if period == "1d" and len(df) >= 2:
                ret = ((df.iloc[-1] - df.iloc[-2]) / df.iloc[-2]) * 100
            elif period == "7d" and len(df) >= 7:
                ret = ((df.iloc[-1] - df.iloc[-7]) / df.iloc[-7]) * 100
            elif period == "30d" and len(df) >= 30:
                ret = ((df.iloc[-1] - df.iloc[-30]) / df.iloc[-30]) * 100
            else:
                ret = 0.0
            returns[ticker] = ret
        except:
            returns[ticker] = 0.0

    # Sort returns
    sorted_returns = sorted(returns.items(), key=lambda x: x[1], reverse=True)
    top_gainers = sorted_returns[:10]
    top_losers = sorted_returns[-10:]

    return {"top_gainers": top_gainers, "top_losers": top_losers}

def get_finance_data():
    """
    Returns structured JSON-like output for 1 day, 1 week, 1 month
    """
    return {
        "1 day": calculate_returns("1d"),
        "1 week": calculate_returns("7d"),
        "1 month": calculate_returns("30d")
    }

if __name__ == "__main__":
    import json
    data = get_finance_data()
    print(json.dumps(data, indent=4))
