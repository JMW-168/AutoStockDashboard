"""市場儀表板的觀察清單設定。"""

MARKET_SECTIONS = [
    {
        "key": "global_indices",
        "title": "全球主要指數",
        "description": "用美國主要股市指數觀察市場方向以利判斷對台股的影響。",
        "symbols": [
            {"ticker": "^GSPC", "name": "S&P 500"},
            {"ticker": "^IXIC", "name": "NASDAQ Composite"},
            {"ticker": "^SOX", "name": "PHLX Semiconductor Index"},
            {"ticker": "^KS11", "name": "KOSPI Composite"},
        ],
    },
    {
        "key": "ai_semiconductors",
        "title": "AI 半導體",
        "description": "追蹤美國核心 AI 與半導體相關股票。",
        "symbols": [
            {"ticker": "NVDA", "name": "NVIDIA"},
            {"ticker": "AMD", "name": "AMD"},
            {"ticker": "AVGO", "name": "Broadcom"},
            {"ticker": "TSM", "name": "TSMC ADR"},
        ],
    },
    {
        "key": "macro",
        "title": "總體經濟指標",
        "description": "觀察美元與債券市場訊號。",
        "symbols": [
            {"ticker": "DX-Y.NYB", "name": "US Dollar Index"},
            {"ticker": "^TNX", "name": "US 10Y Treasury Yield"},
        ],
    },
    {
        "key": "taiwan_market",
        "title": "台灣市場",
        "description": "追蹤台灣股市與重要半導體參考標的。",
        "symbols": [
            {"ticker": "^TWII", "name": "TAIEX"},
            {"ticker": "2330.TW", "name": "TSMC Taiwan"},
        ],
    },
]


DEFAULT_PERIOD = "6mo"
DEFAULT_INTERVAL = "1d"
