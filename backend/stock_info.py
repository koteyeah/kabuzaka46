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

    return ratio, stock_avg_close, current_stock_close
def find_rank_by_index(array, index):
    # 指定されたインデックスの要素を取得
    target_value = array[index]
    # 配列をコピーしてソート
    sorted_array = sorted(array, reverse=True)
    # ソートされた配列での位置（ランク）を検索
    rank = sorted_array.index(target_value) + 1  # インデックスは0から始まるため、ランクは+1する
    return rank


nikkei_tickers=[
    "4151","4502","4503","4506","4507","4519","4523","4568","4578","6479", "6501", "6503", "6504", "6506", "6526", "6594", "6645", "6674", "6701", "6702", "6723", "6724", "6752", "6753", "6758", "6762", "6770", "6841", "6857", "6861", "6902", "6920", "6952", "6954", "6971", "6976", "6981", "7735", "7751", "7752", "8035","7201", "7202", "7203", "7205", "7211", "7261", "7267", "7269", "7270", "7272", "4543", "4902", "6146", "7731", "7733", "7741", "7762", "9432", "9433", "9434", "9613", "9984", "5831", "7186", "8304", "8306", "8308", "8309", "8316", "8331", "8354", "8411", "8253", "8591", "8697", "8601", "8604", "8630", "8725", "8750", "8766", "8795", "1332", "2002", "2269", "2282", "2501", "2502", "2503", "2801", "2802", "2871", "2914", "3086", "3092", "3099", "3382", "8233", "8252", "8267", "9843", "9983", "2413", "2432", "3659", "4324", "4385", "4661", "4689", "4704", "4751", "4755", "6098", "6178", "7974", "9602", "9735", "9766", "1605", "3401", "3402", "3861", "3863", "3405", "3407", "4004", "4005", "4021", "4042", "4043", "4061", "4063", "4183", "4188", "4208", "4452", "4631", "4901", "4911", "6988", "5019", "5020", "5101", "5108", "5201", "5214", "5233", "5301", "5332", "5333", "5401", "5406", "5411", "3436", "5706", "5711", "5713", "5714", "5801", "5802", "5803", "2768", "8001", "8002", "8015", "8031", "8053", "8058", "1721", "1801", "1802", "1803", "1808", "1812", "1925", "1928", "1963", "5631", "6103", "6113", "6273", "6301", "6302", "6305", "6326", "6361", "6367", "6471", "6472", "6473", "7004", "7011", "7013","7012", "7832", "7911", "7912", "7951", "3289", "8801", "8802", "8804", "8830", "9001", "9005", "9007", "9008", "9009", "9020", "9021", "9022", "9064", "9147", "9101", "9104", "9107", "9201", "9202", "9301", "9501", "9502", "9503", "9531", "9532"
]

trade_ratios=[]
market_caps=[]
stock_ratios=[]
stock_avg_closes=[]
current_stock_closes=[]
for code in nikkei_tickers:
    # 出来高の計算
    trade_ratio=calculate_trade_ratio(code)
    trade_ratios.append(trade_ratio)
    # 市場価値の計算
    market_cap=get_market_cap(code)
    market_caps.append(market_cap)
    ratio, stock_avg_close, current_stock_close=calculate_avg_to_current_ratio(code)
    stock_ratios.append(ratio)
    stock_avg_closes.append(stock_avg_close)
    current_stock_closes.append(current_stock_close)
    print(code)
app = FastAPI()

# CORS設定
origins = [
    "http://localhost",
    "http://localhost:3000",  # ReactなどのフロントエンドのURL
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/stock-info/{stock_number}")
async def get_stock_info(stock_number: str):
    ticker = stock_number + ".T"
    # 銘柄の存在を確認
    if not yf.Ticker(ticker).history(period="1d").empty:
        index=nikkei_tickers.index(stock_number)
        trade_ratio_rank=find_rank_by_index(trade_ratios,index)
        trade_ratio_value=trade_ratio_rank/225
        market_cap_rank=find_rank_by_index(market_caps,index)
        market_cap_value=market_cap_rank/225
        stock_ratio_rank=find_rank_by_index(stock_ratios,index)
        stock_ratio_value=stock_ratio_rank/225
        stock = yf.Ticker(ticker)
        info = stock.info
        # ここからレコメンド
        # nogizaka_tracks_features2.csvを読み込む
        df = pd.read_csv('nogizaka_tracks_features2.csv')
        # 2乗誤差を計算
        df['squared_error'] = ((market_cap_value - df['popularity_normalized'])*1.1)**2 + \
                            (stock_ratio_value - df['valence_normalized'])**2 + \
                            ((trade_ratio_value - df['energy_tempo_normalized'])*1.4)**2

        # 2乗誤差の合計が最小の行を取得
        min_error_row = df.loc[df['squared_error'].idxmin()]

        print(min_error_row)
        return {
            "会社名": info.get('longName', '情報が見つかりませんでした'),  # longNameが存在しない場合はデフォルトのメッセージを表示
            "業種": info.get('sector', '情報が見つかりませんでした'),
            "前日終値": info.get('previousClose', '情報が見つかりませんでした'),
            "市場価値": info.get('marketCap', '情報が見つかりませんでした'),
            "current_stock_close":current_stock_closes[index],
            "stock_avg_close":stock_avg_closes[index],
            "stock_ratio": stock_ratios[index],
            "trade_ratio_rank": trade_ratio_rank,
            "trade_ratio_value": trade_ratio_value,
            "market_cap_rank":market_cap_rank,
            "market_cap_value":market_cap_value,
            "stock_ratio_rank":stock_ratio_rank,
            "stock_ratio_value":stock_ratio_value,
            "recommend_music":min_error_row['track_name'],
            "preview_url":min_error_row['preview_url'],
            # "popularity":min_error_row['popularity'],
            # "valence":min_error_row['valence'],
            # "danceability":min_error_row['danceability'],
            # "energy":min_error_row['energy'],
            # "tempo":min_error_row['tempo']
            
        }
    else:
        raise HTTPException(status_code=404, detail="指定された銘柄の情報が見つかりませんでした")
