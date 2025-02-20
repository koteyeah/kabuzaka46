from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import pandas as pd

def get_stock_name(code):
    try:
        stock_info = yf.Ticker(code+".T").info
        stock_name = stock_info['shortName']
    except KeyError:
        stock_name = "Name not found"
    return stock_name
def get_market_cap(code):
    try:
        stock_info = yf.Ticker(code + ".T").info
        market_cap = stock_info['marketCap']
        return market_cap
    except KeyError:
        market_cap="Market cap not found"
        return market_cap
def calculate_trade_ratio(code):
    # yfinanceを使用して株情報を取得
    ticker = yf.Ticker(code+".T")
    info = ticker.info
    volume = info.get('regularMarketVolume', None)
    shares_outstanding = info.get('sharesOutstanding', None)
    # データが存在する場合に割合を計算
    if volume is not None and shares_outstanding is not None:
        trade_ratio = (volume / shares_outstanding) * 100
        formatted_trade_ratio = "{:.4g}".format(trade_ratio)
        return formatted_trade_ratio
    else:
        return 0
def calculate_avg_to_current_ratio(code):
    stock_symbol=code+".T"
    # 現在の日付と1ヶ月前の日付を取得
    end_date = pd.Timestamp.today()
    start_date = end_date - pd.DateOffset(months=1)

    # yfinanceを使用して株価データをダウンロード
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

    # 株価データの終値を使用して平均を計算
    stock_avg_close = stock_data['Close'].mean()

    # 現在の株価を取得
    current_stock_data = yf.download(stock_symbol, period='1d')
    current_stock_close = current_stock_data['Close'].iloc[0]

    # 平均株価と現在の株価の比を計算
    ratio = current_stock_close/stock_avg_close

    return ratio, stock_avg_close
def find_rank_by_index(array, index):
    # 指定されたインデックスの要素を取得
    target_value = array[index]
    # 配列をコピーしてソート
    sorted_array = sorted(array, reverse=True)
    # ソートされた配列での位置（ランク）を検索
    rank = sorted_array.index(target_value) + 1  # インデックスは0から始まるため、ランクは+1する
    return rank
nikkei_tickers=[
    "4151","4502","4503","4506","4507","4519","4523","4568","4578","6479", "6501"]

trade_ratios=[]
market_caps=[]
stock_ratios=[]
stock_avg_closes=[]
current_stock_closes=[]
names=[]
for code in nikkei_tickers:
    names.append(get_stock_name(code))
    market_caps.append(get_market_cap(code))
    trade_ratios.append(calculate_trade_ratio(code))
    ratio,stock_avg_close=calculate_avg_to_current_ratio(code)
    stock_ratios.append(ratio)
    stock_avg_closes.append(stock_avg_close)
print(names)
print(market_caps)
print(trade_ratios)
print(find_rank_by_index(market_caps,0))
print(stock_ratios)
