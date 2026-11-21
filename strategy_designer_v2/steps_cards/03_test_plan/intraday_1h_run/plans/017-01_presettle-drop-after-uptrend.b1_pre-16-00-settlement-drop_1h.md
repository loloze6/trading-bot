---
idea: 017-01_presettle-drop-after-uptrend.b1_pre-16-00-settlement-drop
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: a1c2ac068edc
---
Fidelity:
- Situation: a coin with a strong 3-day run up -> adapted: "strong" is made graded, as the 72-bar rise in percent.
- Comparison: the pre-settlement return is negative, and larger the stronger the rise -> kept: the return is judged against zero, net of the coin's average return.
- Outcome: the return over the 2 hours before the 16:00 UTC settlement declines -> kept: the position is held only over the bars stamped 14:00 and 15:00.
- Verdict transfer: yes: the test measures this rise, this window and this direction, and only "strong" is softened into a grade.
Forecast: The forecast is active only on the two bars whose holding period ends at the 16:00 UTC settlement. These are the bars whose coming bar starts at 14:00 or 15:00 UTC, read by `HourOfDayComponent`. On those bars the forecast is minus the coin's 72-bar (3-day) percent rise, standardised over its past 72 values and then clipped at 0. It is short in proportion to the 3-day rise and 0 when the coin fell, so it never goes long. On every other hour it is 0 (flat).
Config: 017-01_presettle-drop-after-uptrend.b1_pre-16-00-settlement-drop_1h_config.json
Criterion:
- Horizon: 2 bars
- Main measure: There is one case per day per coin and window: the bar stamped 13:00 UTC. For each case, take its forecast f (the value at 14:00) and the excess return y. y is close[t+2] / close[t] - 1 minus the coin's mean 2-bar return over all windows together (non-overlapping grid). Over the cases with f < 0, measure the mean of (f / 10) x y and its t.
- Supporting check: The cases with f < 0 are split into halves by |f|. The mean y of the larger-|f| half minus the mean y of the smaller half must be below 0.
- Confirm: The main mean is above 0 with t ≥ 2, and the supporting check passes.
- Reject: The main mean is below 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is t ≥ 2 with the check failing. At least 500 cases with f < 0 are needed, pooled over coins and windows.
