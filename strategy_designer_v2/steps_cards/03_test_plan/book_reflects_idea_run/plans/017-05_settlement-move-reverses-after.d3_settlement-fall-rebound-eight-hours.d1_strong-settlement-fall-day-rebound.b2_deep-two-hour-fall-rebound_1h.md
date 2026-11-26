---
idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 453ddf5ae165
---
Phase A (runs/BOOK_REFLECTS_IDEA_RUN.md): this plan's config with one rule added: a threshold_filter at 20 after standardise (the situation is present when the score is at least twice its usual size; otherwise no position).
Fidelity:
- Situation: a fall over the coin's last 2 hours, at any hour of the day -> adapted: "after a 2-hour fall" made "while the 2-hour return is negative", graded by its size.
- Comparison: the fall's size against the coin's usual 2-hour move -> kept: the 2-bar return divided by the mean absolute 2-bar return over the last 720 bars.
- Outcome: the next 24 hours run upward, more so after larger falls -> kept: a long held 24 bars that grows with the scaled fall.
- Verdict transfer: yes: the forecast is the scaled 2-hour fall itself, held for the idea's 24 hours, so a confirm or a reject of the size-to-rebound relation is one for the idea.
Forecast: One component, `MeanAbsScaledReturnComponent` with period 2 and window 720. It gives the last 2-hour return in units of the coin's usual 2-hour move, the mean absolute 2-bar return over 30 days. It is standardised against its own past 500 values, then negated so that falls read positive, then clipped at 0. The forecast is positive only after a 2-hour fall and grows linearly with that fall's size in usual moves, up to the cap of 20. It is 0 after a flat or rising 2 hours. It is never negative. There is no clock condition: every hour counts.
Config: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: The sample is the non-overlapping 24-bar grid of each window, using grid bars with forecast > 0 (the cases). For each case, take the coin's 24-bar forward return minus its normal drift, the mean 24-bar return over all windows. Pool the cases over coins and windows. Regress this excess return on the forecast (`post_pipeline_value`). The measure is the slope and its t.
- Supporting check: Take the cases in the top quintile of forecast. Their mean excess 24-bar return, in the long direction, must be above 0.
- Confirm: The slope is positive with t >= 2, and the top-quintile mean excess return is above 0.
- Reject: The slope is negative with t <= -2.
- Inconclusive: Any slope t between -2 and 2 is inconclusive. So is a slope with t >= 2 whose top-quintile mean excess return is at or below 0. The test needs at least 300 cases pooled, with at least 60 in the top quintile; fewer is inconclusive.
