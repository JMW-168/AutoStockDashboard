from __future__ import annotations

import pandas as pd
import streamlit as st

from config.watchlist import DEFAULT_INTERVAL, DEFAULT_PERIOD, MARKET_SECTIONS
from services.market_data import QuoteSnapshot, build_section_snapshots


st.set_page_config(
    page_title="市場儀表板",
    layout="wide",
)


@st.cache_data(ttl=900, show_spinner=False)
def load_section_data(
    symbols: list[dict[str, str]],
    period: str, 
    interval: str,
) -> list[QuoteSnapshot]:
    return build_section_snapshots(symbols, period=period, interval=interval)


def format_number(value: float | None, digits: int = 2) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    return f"{value:,.{digits}f}"


def format_delta(snapshot: QuoteSnapshot) -> str | None:
    if snapshot.change is None or snapshot.change_percent is None:
        return None
    return f"{snapshot.change:+,.2f} ({snapshot.change_percent:+.2f}%)"


def render_snapshot_card(snapshot: QuoteSnapshot) -> None:
    label = f"{snapshot.name} ({snapshot.ticker})"
    st.metric(label=label, value=format_number(snapshot.price), delta=format_delta(snapshot))

    if snapshot.error:
        st.caption(f"資料狀態：{snapshot.error}")
        return

    if not snapshot.history.empty and "Close" in snapshot.history:
        st.line_chart(snapshot.history["Close"], height=120)


def render_section(section: dict[str, object], period: str, interval: str) -> None:
    st.subheader(str(section["title"]))
    st.caption(str(section["description"]))

    snapshots = load_section_data(
        symbols=section["symbols"],  # type: ignore[arg-type]
        period=period,
        interval=interval,
    )

    columns = st.columns(min(len(snapshots), 4))
    for index, snapshot in enumerate(snapshots):
        with columns[index % len(columns)]:
            render_snapshot_card(snapshot)


def main() -> None:
    st.title("市場儀表板")
    st.caption("這是一個使用 Streamlit 製作的市場資料儀表板，用來追蹤全球指數、AI 半導體、總體經濟訊號與台灣市場資料。")

    with st.sidebar:
        st.header("設定")
        period = st.selectbox(
            "歷史資料範圍",
            options=["1mo", "3mo", "6mo", "1y", "2y"],
            index=["1mo", "3mo", "6mo", "1y", "2y"].index(DEFAULT_PERIOD),
            format_func={
                "1mo": "1 個月",
                "3mo": "3 個月",
                "6mo": "6 個月",
                "1y": "1 年",
                "2y": "2 年",
            }.get,
        )
        interval = st.selectbox(
            "資料間隔",
            options=["1d", "1wk", "1mo"],
            index=["1d", "1wk", "1mo"].index(DEFAULT_INTERVAL),
            format_func={
                "1d": "每日",
                "1wk": "每週",
                "1mo": "每月",
            }.get,
        )

        if st.button("重新整理資料", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    for section in MARKET_SECTIONS:
        render_section(section, period=period, interval=interval)
        st.divider()


if __name__ == "__main__":
    main()
