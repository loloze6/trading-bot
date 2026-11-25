---
idea: 037-02_fall-range-beyond-loss-rebound
brief: 037_wide-range-separates-forced-falls
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 00d5d6f5c07b
---
Fidelity:
- Situation: a coin's one-day fall, larger the more it fell -> kept: the fall from the prior close is measured on bar t's own bars.
- Comparison: the day's high-to-low range against the closing loss itself -> kept in kind: NetMoveToRangeRatioComponent (period 1) gives loss / range, but nothing combines it jointly with the fall size.
- Outcome: a larger rise over the next day -> kept: 1 bar on daily bars, long only.
- Verdict transfer: no: no config built from the catalogue keeps "taken together" and also stays long only, so no plan carries the verdict.
Reason: The closing loss over range is available (NetMoveToRangeRatioComponent, period 1), but the forecast is a weighted sum, so it cannot form the joint product of fall size and excess range. A sum with that ratio needs a centring constant that pushes the forecast below zero on falls with a narrow range, which breaks the brief's long-only rule. The catalogue's fall-times-range components measure range against recent ranges (RiseTimesRangeMultipleComponent) or the close's place in the bar (FallCloseLocationComponent), not against the closing loss.
