from __future__ import annotations

import streamlit as st


FEATURE_LOG = [
    {
        "version": "v0.2.0",
        "title": "版面導覽與功能紀錄",
        "items": [
            "將歷史資料範圍與資料間隔移到主標題下方。",
            "新增右上角版本號與程式上次更新日期。",
            "將側邊欄改為頁面切換，並新增開發歷程頁。",
        ],
    },
    {
        "version": "v0.1.0",
        "title": "市場交易儀表板初版",
        "items": [
            "建立市場指數、AI 半導體、總體經濟與台灣市場區塊。",
            "加入近期交易資料表與 K 線圖。",
            "使用 yfinance 擷取並快取市場資料。",
        ],
    },
]


def render_changelog_page() -> None:
    st.subheader("開發歷程")
    st.caption("用版本節點追蹤儀表板陸續加入的功能。")

    entries = []
    for entry in FEATURE_LOG:
        items = "".join(f"<li>{item}</li>" for item in entry["items"])
        entries.append(
            '<div class="feature-entry">'
            '<div class="feature-node"></div>'
            f'<div class="feature-version">{entry["version"]}</div>'
            f'<div class="feature-title">{entry["title"]}</div>'
            f'<ul class="feature-items">{items}</ul>'
            '</div>'
        )

    st.markdown(f'<div class="feature-log">{"".join(entries)}</div>', unsafe_allow_html=True)
