---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: the coin's 7-day return, larger meaning stronger -> kept
- Comparison: only while the coin's 30-day return is positive -> kept
- Outcome: the next 7 days' return is higher the larger the 7-day return -> kept
- Verdict transfer: yes: the test measures this exact relation inside this exact condition, at the idea's own horizon.
Forecast: A regime rule sets "trending" while the 30-bar price change is above 0; every other bar is flat. Inside that regime, the forecast is the 7-bar price change, standardised against its own past 60 values and clipped at 0. It is long only. It grows in proportion to how strong the past week was. It is zero when the week was flat or down, which matches "stay out".
Config: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1d_config.json
Criterion:
- Horizon: 7 bars
- Main measure: Use only bars with regime "trending", sampled on the non-overlapping 7-bar grid of each window and pooled over coins. Regress each bar's 7-bar forward return, minus that coin's mean 7-bar return over all windows, on the raw 7-day return (`r7.last_history_value`). Report the slope's t.
- Supporting check: The timing part of the book's mean daily gain is above 0. This is the book's mean gain minus the gain from the market's own rise.
- Confirm: The slope's t is 2 or more, with at least 100 independent cases, and the supporting check passes.
- Reject: The slope's t is -2 or less, with at least 100 independent cases.
- Inconclusive: Any t between -2 and 2, or a confirming t when the supporting check fails, is inconclusive. Fewer than 100 independent grid cases in the regime is also inconclusive.
