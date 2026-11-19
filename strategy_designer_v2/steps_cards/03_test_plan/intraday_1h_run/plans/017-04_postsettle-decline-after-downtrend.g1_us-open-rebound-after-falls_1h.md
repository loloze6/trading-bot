---
idea: 017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a coin with a 3-day fall, at 12:00 UTC -> adapted: the 72-bar fall is graded by its depth (zero after a rise), and the clock is a regime on the coming bar's hour.
- Comparison: deeper fall versus shallower fall -> kept: the position size grows with the percent depth of the 72-bar fall.
- Outcome: the return over the 2 hours from 12:00 UTC is positive, larger after deeper falls -> kept: long only over the 12:00 and 13:00 bars, flat on every other bar.
- Verdict transfer: yes: the position is exactly long the 12:00–14:00 return, sized by the 3-day fall, so its gain confirms or rejects the idea.
Forecast: The regime is active when the coming bar starts at 12:00 or 13:00 UTC, which are the decisions at the closes of the 11:00 and 12:00 bars. In that regime the forecast is the 72-bar percent price change, standardised against its own last 72 values, negated, and clipped at 0. It is positive and grows with the depth of the 3-day fall. It is 0 when the coin rose over the 3 days, and 0 at every other hour. It is never short.
Config: 017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls_1h_config.json
Criterion:
- Horizon: 2 bars
- Main measure: One case per coin-day, inside one window. A case is the bar stamped 11:00 UTC whose forecast is above 0. For each case, take (forecast / 10) × (close of the 13:00 bar / close of the 11:00 bar − 1 − the coin's mean 2-bar return over all windows). The measure is the mean of these values pooled over coins, with its ordinary t.
- Supporting check: Regress the same excess 2-bar return on the forecast over the same cases. The slope must be above 0.
- Confirm: The main measure has a mean above 0 with t ≥ 2, and the slope is above 0.
- Reject: The main measure has a mean below 0 with t ≤ −2.
- Inconclusive: Any t between −2 and 2 is inconclusive. So is a t ≥ 2 with a slope of 0 or below. At least 300 cases are required; fewer is inconclusive.
