---
idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_one-day-fall-multi-day-rebound
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: how far the coin has fallen over its last 24 hours -> kept
- Comparison: none (the idea states the depth of the fall and its graded effect, with no benchmark) -> kept
- Outcome: price rises over the next 3 days, more after deeper falls -> kept
- Verdict transfer: yes: the forecast grows with the 24-hour fall and is held for 3 days, so the test measures the stated graded relation directly.
Forecast: One indicator, the 24-bar percent change of the close (PriceEvolutionComponent, period 24). Standardise puts it on the scale of its own last 60 values (60/20). Negate turns a fall into a positive value. A clip at 0 removes rises, so the forecast is zero after a 24-hour rise, and the idea says nothing about rises. After a 24-hour fall the forecast is positive (long), and it grows smoothly with the depth of the fall, up to the cap of 20. It is never negative.
Config: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_one-day-fall-multi-day-rebound_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: Use the bars at positions 0, 72, 144, ... of each window. On those bars, take the coin's return over the next 72 bars minus the coin's mean 72-bar return over all its windows. Regress that excess return on `forecast`, pooled over coins and windows, and test the slope with its t-statistic.
- Supporting check: The book's mean daily return before costs, minus its gain from the market's own rise, is above 0. This is the timing part of the book's return, as the workflow defines it.
- Confirm: The slope is positive with t >= 2, and the supporting check passes.
- Reject: The slope is negative with t <= -2.
- Inconclusive: Any slope with t between -2 and 2, or a confirming slope whose timing check fails. The test also needs at least 200 grid cases with forecast > 0, out of about 5,800 grid cases in total; with fewer, the result is inconclusive.
