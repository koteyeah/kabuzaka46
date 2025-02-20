"use client";
import { useState } from "react";
import Loading from "./components/Loading";
import { nikkei_names, nikkei_tickers } from "./codes";

export default function Home() {
  const [stockNumber, setStockNumber] = useState("");
  const [selectedCompany, setSelectedCompany] = useState("");
  const [loading, setLoading] = useState(false);
  const [stockData, setStockData] = useState(null);
  const cardStyle =
    "p-4 bg-gray-50 shadow-lg rounded-lg transform transition duration-200 hover:scale-105";
  const handleCompanyChange = (e) => {
    const selectedName = e.target.value;
    setSelectedCompany(selectedName);

    const index = nikkei_names.indexOf(selectedName);
    if (index !== -1) {
      setStockNumber(nikkei_tickers[index]);
    } else {
      setStockNumber("");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);
    setStockData(null);

    try {
      const response = await fetch(
        `http://localhost:8000/stock-info/${stockNumber}`
      );

      if (!response.ok) {
        setLoading(false);
        if (response.status === 404) {
          alert("指定された銘柄の情報が見つかりませんでした。");
        } else {
          alert("サーバーエラーが発生しました。");
        }
        return;
      }

      const data = await response.json();
      setStockData(data);
      setLoading(false);
    } catch (error) {
      console.error("エラーが発生しました:", error);
      alert("予期しないエラーが発生しました。");
      setLoading(false);
    }
  };

  return (
    <>
      <img src="Header.png" className="max-w-sm mx-auto" />
      <main className="flex flex-col items-center min-h-screen">
        <h1 className="text-4xl p-3 m-3">
          あなたの入力した株に近い乃木坂の曲をレコメンドします
        </h1>
        <form onSubmit={handleSubmit} className="text-center">
          <select
            value={selectedCompany}
            onChange={handleCompanyChange}
            className="m-4 p-2 border-2 border-gray-300 rounded-md shadow-sm focus:outline-none focus:border-red-200"
          >
            <option value="">会社名を選択してください</option>
            {nikkei_names.map((name, index) => (
              <option key={index} value={name}>
                {name}
              </option>
            ))}
          </select>
          <button
            type="submit"
            className="px-4 py-2 bg-red-400 text-white font-semibold rounded-md shadow hover:bg-red-500 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50"
          >
            検索
          </button>{" "}
        </form>

        {loading && <Loading />}

        {stockData && (
          <div className="flex p-5 border-4 border-slate-200 shadow-lg rounded-lg">
            {" "}
            <div className="text-center mx-5">
              <div className="grid grid-cols-2 gap-4">
                <p className={cardStyle}>会社名: {stockData["会社名"]}</p>
                <p className={cardStyle}>業種: {stockData["業種"]}</p>
                <p className={cardStyle}>
                  現在の株価: {stockData["current_stock_close"]}
                </p>
                <p className={cardStyle}>
                  過去一ヶ月の平均株価: {stockData["stock_avg_close"]}
                </p>
                <p className={cardStyle}>市場価値: {stockData["市場価値"]}</p>
                <p className={cardStyle}>
                  市場価値ランキング: {stockData["market_cap_rank"]}
                </p>
                <p className={cardStyle}>
                  値上がり比: {stockData["stock_ratio"]}
                </p>
                <p className={cardStyle}>
                  値上がり比ランキング: {stockData["stock_ratio_rank"]}
                </p>
                <p className={cardStyle}>
                  出来高ランキング: {stockData["trade_ratio_rank"]}
                </p>
              </div>
            </div>
            <div className={cardStyle + "flex flex-col items-center text-lg"}>
              <p className="p-3">{stockData["recommend_music"]}</p>
              <audio controls src={stockData["preview_url"]}>
                Your browser does not support the audio element.
              </audio>
            </div>
          </div>
        )}
      </main>
    </>
  );
}
