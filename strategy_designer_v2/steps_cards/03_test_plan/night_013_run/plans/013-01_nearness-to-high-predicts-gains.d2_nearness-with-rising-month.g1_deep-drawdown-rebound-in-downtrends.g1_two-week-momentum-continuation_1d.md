---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: a coin's 14-day return, the higher the stronger -> kept
- Comparison: higher versus lower 14-day return of the same coin -> kept
- Outcome: a higher return over the next 7 days -> kept
- Verdict transfer: yes: the forecast is the coin's own 14-day return, and the test asks whether larger values come before larger 7-day returns.
Forecast: The forecast is the coin's 14-bar percent return (PriceEvolutionComponent, period 14), standardised against its own past 60 values (min_periods 20). It is positive after a 14-day rise and negative after a 14-day fall. It grows in proportion to the size of the move, is capped at ±20, and is near zero when the 14-day return is near zero. It is active on every bar, with no regime and no dead zone, because the idea is a steady relation.
Config: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation_1d_config.json
Criterion:
- Horizon: 7 bars
- Main measure: Use non-overlapping 7-bar samples (positions 0, 7, 14, ... of each window) pooled over coins and windows. Regress each sample's 7-bar forward return, minus that coin's mean 7-bar return over all windows, on the forecast at the sample bar, and read the t of the slope.
- Supporting check: The book's mean daily gain, minus its gain from the market's own rise (the timing part), is above 0 before costs.
- Confirm: The slope is positive with t ≥ 2, and the timing part of the book's gain is above 0.
- Reject: The slope is negative with t ≤ -2.
- Inconclusive: A slope t between -2 and 2 is inconclusive. So is a slope t ≥ 2 with a timing gain of 0 or below. At least 100 non-overlapping cases are required; about 2,400 are expected.
