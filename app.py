from __future__ import annotations

import streamlit as st

from components.layout import render_global_styles, render_page_header, render_sidebar
from views.changelog import render_changelog_page
from views.dashboard import render_dashboard_page
from views.trade_concept import render_stock_concept_page


APP_VERSION = "v0.5.0"
APP_LAST_UPDATED = "2026-07-10"
DEFAULT_PAGE = "市場交易儀表板"


st.set_page_config(
    page_title="股票市場儀表板",
    layout="wide",
)


def main() -> None:
    render_global_styles()

    if "current_page" not in st.session_state:
        st.session_state.current_page = DEFAULT_PAGE

    st.session_state.current_page = render_sidebar(st.session_state.current_page)

    if st.session_state.current_page == "市場交易儀表板":
        render_page_header(APP_VERSION, APP_LAST_UPDATED)
        render_dashboard_page()
    elif st.session_state.current_page == "進銘的股價概念":
        render_stock_concept_page()
    else:
        render_changelog_page()


if __name__ == "__main__":
    main()
