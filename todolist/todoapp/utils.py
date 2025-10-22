# utils.py
import yfinance as yf

# Financial sector tickers
TICKERS = [
    "HDFCBANK.NS","ICICIBANK.NS","AXISBANK.NS","KOTAKBANK.NS","SBIN.NS",
    "BAJFINANCE.NS","BAJAJFINSV.NS","HDFCLIFE.NS","ICICIPRULI.NS",
    "LICHSGFIN.NS","MUTHOOTFIN.NS","PNB.NS","BANKBARODA.NS","IDFCFIRSTB.NS",
    "FEDERALBNK.NS","RBLBANK.NS","YESBANK.NS","SHRIRAMFIN.NS",
    "PFC.NS","ICICIGI.NS","HDFCAMC.NS","BAJAJHLDNG.NS"
]

def calculate_returns(period="1d"):
    """
    Calculate returns for top gainers and losers for a given period.
    period: '1d', '7d', '30d'
    """
    try:
        # Download data for all tickers at once
        data = yf.download(
            TICKERS,
            period="2mo",
            interval="1d",
            group_by='ticker',
            progress=False,
            threads=True
        )
    except Exception as e:
        print(f"Error downloading data: {e}")
        return {"top_gainers": [], "top_losers": []}

    returns = {}

    for ticker in TICKERS:
        try:
            # Get adjusted close if available, else close
            df = data[ticker].get('Adj Close', data[ticker].get('Close')).dropna()
            if df.empty:
                continue  # Skip ticker with no data

            if period == "1d" and len(df) >= 2:
                ret = ((df.iloc[-1] - df.iloc[-2]) / df.iloc[-2]) * 100
            elif period == "7d" and len(df) >= 7:
                ret = ((df.iloc[-1] - df.iloc[-7]) / df.iloc[-7]) * 100
            elif period == "30d" and len(df) >= 30:
                ret = ((df.iloc[-1] - df.iloc[-30]) / df.iloc[-30]) * 100
            else:
                continue  # Not enough data for this period

            returns[ticker] = ret

        except Exception as e:
            # Skip tickers that cause errors (delisted, missing data)
            print(f"Skipping {ticker}: {e}")
            continue

    # Sort returns
    sorted_returns = sorted(returns.items(), key=lambda x: x[1], reverse=True)
    top_gainers = sorted_returns[:10]
    top_losers = sorted_returns[-10:]

    return {"top_gainers": top_gainers, "top_losers": top_losers}

def get_finance_data():
    """
    Returns structured data for 1 day, 1 week, 1 month
    """
    return {
        "1 day": calculate_returns("1d"),
        "1 week": calculate_returns("7d"),
        "1 month": calculate_returns("30d")
    }

# Test if run standalone
if __name__ == "__main__":
    import json
    data = get_finance_data()
    print(json.dumps(data, indent=4))
