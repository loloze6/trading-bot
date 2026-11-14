---
idea: 002-01_sma-upcross-upward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: short average has just crossed above the long average -> adapted: "after the cross" made "while the 50-day SMA is above the 200-day SMA", graded by the spread.
- Comparison: random points -> kept: forward returns are judged against all bars, which is the coin's own unconditional drift.
- Outcome: price keeps rising over the following bars -> kept: measured as the forward 20-bar return of BTC, upward.
- Verdict transfer: yes: the "while" form of the cross is the guide's allowed adaptation, and its up side is measured directly against random bars.
Forecast: The forecast is (SMA50 − SMA200) / SMA200 on daily closes. It is standardised against its own past 200 values, so a typical spread gives 10. It is then clipped at 0, so it is long-only, matching the idea's upward cross. It is positive while the 50-day average is above the 200-day average. It grows as the short average pulls further above the long one, and is capped at 20. It is zero while the short average is at or below the long one.
Config: 002-01_sma-upcross-upward-drift_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: Regress BTC's next-20-bar log return on the forecast, pooled over the 6 windows. Use Newey-West (lag 19) standard errors so overlapping returns count once. The intercept absorbs the coin's own drift, so the slope is the gain beyond simply holding.
- Supporting check: Take the bars with forecast > 0. Count the share whose next-20-bar return beats the coin's mean 20-bar return over all bars.
- Confirm: Slope t ≥ +2, and the supporting share is above 50%.
- Reject: Slope t ≤ −2: larger spreads are followed by worse-than-average 20-bar returns, so moves after crosses reverse.
- Inconclusive: Any t between −2 and +2 is inconclusive. So is any run with fewer than 10 non-overlapping 20-bar blocks where the forecast is > 0, or fewer than 30 non-overlapping blocks in total.
