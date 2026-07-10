"""市場偏多/中性/偏空的規則式判斷。"""

from __future__ import annotations

from dataclasses import dataclass

from services.market_data import QuoteSnapshot


BULLISH = "偏多"
NEUTRAL = "中性"
BEARISH = "偏空"


@dataclass(frozen=True)
class SectionSignal:
    section_key: str
    label: str
    score: float
    valid_count: int
    reason: str


@dataclass(frozen=True)
class MarketSummary:
    label: str
    score: float
    reason: str


def classify_score(score: float) -> str:
    if score >= 0.35:
        return BULLISH
    if score <= -0.35:
        return BEARISH
    return NEUTRAL


def score_snapshot(snapshot: QuoteSnapshot, section_key: str) -> float | None:
    if snapshot.change_percent is None:
        return None

    score = snapshot.change_percent
    if section_key == "macro":
        score *= -1

    return score


def build_section_signal(section_key: str, snapshots: list[QuoteSnapshot]) -> SectionSignal:
    scores = [
        score
        for snapshot in snapshots
        if (score := score_snapshot(snapshot, section_key)) is not None
    ]

    if not scores:
        return SectionSignal(
            section_key=section_key,
            label=NEUTRAL,
            score=0,
            valid_count=0,
            reason="資料不足，暫以中性看待。",
        )

    average_score = sum(scores) / len(scores)
    label = classify_score(average_score)
    reason = build_section_reason(section_key, label, average_score, len(scores))

    return SectionSignal(
        section_key=section_key,
        label=label,
        score=average_score,
        valid_count=len(scores),
        reason=reason,
    )


def build_market_summary(signals: list[SectionSignal]) -> MarketSummary:
    valid_signals = [signal for signal in signals if signal.valid_count > 0]
    if not valid_signals:
        return MarketSummary(
            label=NEUTRAL,
            score=0,
            reason="目前沒有足夠資料形成市場方向判斷。",
        )

    average_score = sum(signal.score for signal in valid_signals) / len(valid_signals)
    label = classify_score(average_score)
    bullish_count = sum(1 for signal in valid_signals if signal.label == BULLISH)
    bearish_count = sum(1 for signal in valid_signals if signal.label == BEARISH)
    neutral_count = sum(1 for signal in valid_signals if signal.label == NEUTRAL)

    reason = (
        f"目前 {bullish_count} 個區塊偏多、{neutral_count} 個區塊中性、"
        f"{bearish_count} 個區塊偏空，整體分數 {average_score:+.2f}。"
    )

    return MarketSummary(label=label, score=average_score, reason=reason)


def build_section_reason(section_key: str, label: str, score: float, valid_count: int) -> str:
    section_notes = {
        "global_indices": "全球主要指數反映國際風險偏好。",
        "ai_semiconductors": "AI 與半導體指標股牽動台股科技族群情緒。",
        "macro": "美元與美債殖利率上升時，通常對股市估值較不利。",
        "taiwan_market": "台灣市場與台積電走勢反映本地盤勢動能。",
    }
    note = section_notes.get(section_key, "此區塊反映市場方向。")
    return f"{note} 目前以 {valid_count} 筆有效資料計算，分數 {score:+.2f}，判斷為{label}。"
