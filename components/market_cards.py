from __future__ import annotations

import altair as alt
import pandas as pd
import streamlit as st

from services.market_data import QuoteSnapshot


def format_number(value: float | None, digits: int = 2) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    return f"{value:,.{digits}f}"


def format_delta(snapshot: QuoteSnapshot) -> str | None:
    if snapshot.change is None or snapshot.change_percent is None:
        return None
    return f"{snapshot.change:+,.2f} ({snapshot.change_percent:+.2f}%)"


def get_recent_trading_rows(history: pd.DataFrame, days: int = 3) -> pd.DataFrame:
    required_columns = ["Open", "High", "Low", "Close"]
    if history.empty or any(column not in history for column in required_columns):
        return pd.DataFrame()

    recent = history.dropna(subset=required_columns).tail(days).copy()
    if recent.empty:
        return pd.DataFrame()

    if isinstance(recent.index, pd.DatetimeIndex):
        recent["日期"] = recent.index.strftime("%Y-%m-%d")
    else:
        recent["日期"] = recent.index.astype(str)

    recent["開盤價"] = recent["Open"].astype(float)
    recent["最高價"] = recent["High"].astype(float)
    recent["最低價"] = recent["Low"].astype(float)
    recent["收盤價"] = recent["Close"].astype(float)
    recent["漲跌"] = recent["收盤價"] - recent["開盤價"]
    recent["漲跌幅"] = recent["漲跌"] / recent["開盤價"] * 100
    recent["前日收盤價"] = history["Close"].dropna().shift(1).reindex(recent.index).astype(float)
    recent["相對前日漲跌"] = recent["收盤價"] - recent["前日收盤價"]
    recent["相對前日漲跌幅"] = recent["相對前日漲跌"] / recent["前日收盤價"] * 100
    return recent[
        [
            "日期",
            "開盤價",
            "最高價",
            "最低價",
            "收盤價",
            "漲跌",
            "漲跌幅",
            "相對前日漲跌",
            "相對前日漲跌幅",
        ]
    ]


def render_candlestick_chart(recent_rows: pd.DataFrame) -> None:
    base = alt.Chart(recent_rows).encode(
        x=alt.X("日期:N", sort=None, axis=alt.Axis(title=None, labelAngle=0)),
        color=alt.condition(
            "datum['收盤價'] >= datum['開盤價']",
            alt.value("#ef4444"),
            alt.value("#22c55e"),
        ),
    )

    wick = base.mark_rule().encode(
        y=alt.Y("最低價:Q", scale=alt.Scale(zero=False), axis=alt.Axis(title=None)),
        y2="最高價:Q",
    )
    body = base.mark_bar(size=28).encode(
        y="開盤價:Q",
        y2="收盤價:Q",
    )

    st.altair_chart((wick + body).properties(height=180), use_container_width=True)


def render_snapshot_card(snapshot: QuoteSnapshot) -> None:
    label = f"{snapshot.name} ({snapshot.ticker})"
    st.metric(
        label=label,
        value=format_number(snapshot.price),
        delta=format_delta(snapshot),
        delta_color="inverse",
    )

    if snapshot.error:
        st.caption(f"資料狀態：{snapshot.error}")
        return

    recent_rows = get_recent_trading_rows(snapshot.history)
    if not recent_rows.empty:
        st.dataframe(
            pd.DataFrame(
                {
                    "日期": recent_rows["日期"],
                    "收盤價": recent_rows["收盤價"].map(format_number),
                    "漲跌": recent_rows["相對前日漲跌"].map(
                        lambda value: "N/A" if pd.isna(value) else format_number(value)
                    ),
                    "漲跌幅": recent_rows["相對前日漲跌幅"].map(
                        lambda value: "N/A" if pd.isna(value) else f"{value:+.2f}%"
                    ),
                }
            ),
            hide_index=True,
            use_container_width=True,
            height=145,
        )
        render_candlestick_chart(recent_rows)
