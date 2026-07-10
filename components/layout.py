from __future__ import annotations

import streamlit as st


def render_global_styles() -> None:
    st.markdown(
        """
        <style>
            .app-version {
                color: #64748b;
                font-size: 0.84rem;
                font-weight: 500;
                line-height: 1.6;
                padding-top: 0.7rem;
                text-align: right;
            }
            .app-version strong {
                color: #0f172a;
                font-size: 0.92rem;
                font-weight: 700;
            }
            section[data-testid="stSidebar"] div.stButton > button {
                background: transparent;
                border: 0;
                border-radius: 6px;
                color: #334155;
                font-size: 1rem;
                font-weight: 600;
                justify-content: flex-start;
                padding: 0.65rem 0.8rem;
                text-align: left;
            }
            section[data-testid="stSidebar"] div.stButton > button:hover {
                background: #e0f2fe;
                color: #0369a1;
            }
            section[data-testid="stSidebar"] div.stButton > button:focus {
                box-shadow: none;
            }
            .feature-log {
                margin-top: 1.5rem;
                max-width: 920px;
            }
            .feature-entry {
                border-left: 2px solid #94a3b8;
                margin-left: 0.55rem;
                padding: 0 0 1.4rem 1.5rem;
                position: relative;
            }
            .feature-entry:last-child {
                padding-bottom: 0;
            }
            .feature-node {
                background: #0f172a;
                border: 3px solid #38bdf8;
                border-radius: 999px;
                height: 0.9rem;
                left: -0.52rem;
                position: absolute;
                top: 0.15rem;
                width: 0.9rem;
            }
            .feature-version {
                color: #0369a1;
                font-size: 0.85rem;
                font-weight: 700;
                letter-spacing: 0;
                margin-bottom: 0.2rem;
            }
            .feature-title {
                color: #0f172a;
                font-size: 1.1rem;
                font-weight: 700;
                margin-bottom: 0.35rem;
            }
            .feature-items {
                color: #334155;
                line-height: 1.75;
                margin: 0;
                padding-left: 1.1rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(app_version: str, last_updated: str) -> None:
    title_column, version_column = st.columns([0.82, 0.18], vertical_alignment="top")
    with title_column:
        st.title("市場交易儀表板")
        st.caption("這是一個股票資料儀表板，用來協助交易員了解近期的市場經濟訊號與台灣市場資料。")
    with version_column:
        st.markdown(
            f"""
            <div class="app-version">
                <strong>{app_version}</strong><br>
                程式上次更新：{last_updated}
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_sidebar(current_page: str) -> str:
    selected_page = current_page

    with st.sidebar:
        if st.button("市場交易儀表板", use_container_width=True):
            selected_page = "市場交易儀表板"
        if st.button("開發歷程", use_container_width=True):
            selected_page = "開發歷程"

    return selected_page
