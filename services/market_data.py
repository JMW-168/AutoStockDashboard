"""透過 yfinance 取得市場資料的服務層。"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import yfinance as yf


@dataclass(frozen=True)
class QuoteSnapshot:
    ticker: str
    name: str
    price: float | None
    change: float | None
    change_percent: float | None
    history: pd.DataFrame
    error: str | None = None


def fetch_history(ticker: str, period: str = "6mo", interval: str = "1d") -> pd.DataFrame:
    """取得單一 ticker 的歷史 OHLCV 資料。"""
    data = yf.download(
        tickers=ticker,
        period=period,
        interval=interval,
        progress=False,
        auto_adjust=False,
        threads=False,
    )

    if data.empty:
        return pd.DataFrame()

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    return data.dropna(how="all")


def build_snapshot(
    ticker: str,
    name: str,
    period: str = "6mo",
    interval: str = "1d",
) -> QuoteSnapshot:
    """建立儀表板顯示所需的最新報價與歷史資料。"""
    try:
        history = fetch_history(ticker, period=period, interval=interval)
    except Exception as exc:  # yfinance can raise transport and parsing errors.
        return QuoteSnapshot(ticker, name, None, None, None, pd.DataFrame(), str(exc))

    if history.empty or "Close" not in history:
        return QuoteSnapshot(ticker, name, None, None, None, history, "沒有取得資料")

    close = history["Close"].dropna()
    if close.empty:
        return QuoteSnapshot(ticker, name, None, None, None, history, "沒有收盤價資料")

    latest = float(close.iloc[-1])
    previous = float(close.iloc[-2]) if len(close) > 1 else latest
    change = latest - previous
    change_percent = (change / previous * 100) if previous else 0.0

    return QuoteSnapshot(ticker, name, latest, change, change_percent, history)


def build_section_snapshots(
    symbols: list[dict[str, str]],
    period: str = "6mo",
    interval: str = "1d",
) -> list[QuoteSnapshot]:
    """取得儀表板區塊中所有標的的資料快照。"""
    return [
        build_snapshot(symbol["ticker"], symbol["name"], period=period, interval=interval)
        for symbol in symbols
    ]
