from __future__ import annotations

import streamlit as st

from components.market_cards import render_snapshot_card
from config.watchlist import DEFAULT_INTERVAL, DEFAULT_PERIOD, MARKET_SECTIONS
from services.market_data import QuoteSnapshot, build_section_snapshots
from services.signal_rules import MarketSummary, SectionSignal, build_market_summary, build_section_signal


PERIOD_OPTIONS = ["1mo", "3mo", "6mo", "1y", "2y"]
INTERVAL_OPTIONS = ["1d", "1wk", "1mo"]


@st.cache_data(ttl=900, show_spinner=False)
def load_section_data(
    symbols: list[dict[str, str]],
    period: str,
    interval: str,
) -> list[QuoteSnapshot]:
    return build_section_snapshots(symbols, period=period, interval=interval)


def render_data_controls() -> tuple[str, str]:
    period_column, interval_column, refresh_column = st.columns([0.24, 0.24, 0.52], vertical_alignment="bottom")
    with period_column:
        period = st.selectbox(
            "歷史資料範圍",
            options=PERIOD_OPTIONS,
            index=PERIOD_OPTIONS.index(DEFAULT_PERIOD),
            format_func={
                "1mo": "1 個月",
                "3mo": "3 個月",
                "6mo": "6 個月",
                "1y": "1 年",
                "2y": "2 年",
            }.get,
        )
    with interval_column:
        interval = st.selectbox(
            "資料間隔",
            options=INTERVAL_OPTIONS,
            index=INTERVAL_OPTIONS.index(DEFAULT_INTERVAL),
            format_func={
                "1d": "每日",
                "1wk": "每週",
                "1mo": "每月",
            }.get,
        )
    with refresh_column:
        if st.button("重新整理資料"):
            st.cache_data.clear()
            st.rerun()

    return period, interval


def render_section(section: dict[str, object], period: str, interval: str) -> None:
    snapshots = load_section_data(
        symbols=section["symbols"],  # type: ignore[arg-type]
        period=period,
        interval=interval,
    )

    render_section_with_signal(section, snapshots)


def render_section_with_signal(
    section: dict[str, object],
    snapshots: list[QuoteSnapshot],
    signal: SectionSignal | None = None,
) -> None:
    if signal is None:
        signal = build_section_signal(str(section["key"]), snapshots)

    title_column, signal_column = st.columns([0.8, 0.2], vertical_alignment="top")
    with title_column:
        st.subheader(str(section["title"]))
        st.caption(str(section["description"]))
    with signal_column:
        st.markdown(
            f"""
            <div class="signal-pill signal-{signal.label}">
                {signal.label}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.caption(signal.reason)

    columns = st.columns(min(len(snapshots), 4))
    for index, snapshot in enumerate(snapshots):
        with columns[index % len(columns)]:
            render_snapshot_card(snapshot)


def render_market_summary(summary: MarketSummary, signal_rows: list[tuple[str, SectionSignal]]) -> None:
    signal_items = "".join(
        f"<div><span>{title}</span><strong>{signal.label}</strong></div>"
        for title, signal in signal_rows
    )
    st.markdown(
        f"""
        <div class="market-summary summary-{summary.label}">
            <div class="summary-label">市場總結</div>
            <div class="summary-title">{summary.label}</div>
            <div class="summary-reason">{summary.reason}</div>
            <div class="summary-signals">{signal_items}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_dashboard_page() -> None:
    period, interval = render_data_controls()

    section_states = []
    for section in MARKET_SECTIONS:
        snapshots = load_section_data(
            symbols=section["symbols"],  # type: ignore[arg-type]
            period=period,
            interval=interval,
        )
        signal = build_section_signal(str(section["key"]), snapshots)
        section_states.append((section, snapshots, signal))

    signals = [signal for _, _, signal in section_states]
    signal_rows = [(str(section["title"]), signal) for section, _, signal in section_states]
    render_market_summary(build_market_summary(signals), signal_rows)
    st.divider()

    for section, snapshots, signal in section_states:
        render_section_with_signal(section, snapshots, signal)
        st.divider()
