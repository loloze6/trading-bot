---
idea: 031-02_near-yearly-low-bounces
brief: 031_yearly-low-capitulation-or-exhaustion
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 31f1a8c6c7f6
---
Fidelity:
- Situation: the daily close's nearness to its lowest close of the past 365 days -> kept
- Comparison: closer versus farther from that low ("the closer, the more") -> kept
- Outcome: the price rises more over the next 20 days -> kept
- Verdict transfer: yes: the forecast is the nearness itself, so a 20-day return that grows with it confirms the idea, and one that shrinks with it rejects it.
Forecast: The forecast uses one indicator, DistanceFromHighComponent with `extreme` "low", `source` "close", `period` 365, `exclude_current` 0, `form` "proximity" and `power` 1. Its raw value is 1/(1+D), where D is the close's percent distance above its lowest close of the last 365 days. It is 1 at the low and shrinks toward 0 as the close moves away. `standardise` (window 365, min_periods 91) puts it on the forecast scale. The forecast is always long: small far from the low, rising smoothly as the close nears the low, and capped at +20 at or near it. It is never negative, because the idea claims more rise, not a fall, and the test is judged against holding the coin. It is zero only before warm-up.
Config: 031-02_near-yearly-low-bounces_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: The slope t of a least-squares regression across cases. Each case's excess return is the coin's 20-bar return from bar t minus that coin's mean 20-bar return over all its windows (holding the coin). The regressor is the bar's forecast. Cases are taken on non-overlapping 20-bar grids within each window and pooled over coins, before costs.
- Supporting check: Compare the mean excess 20-bar return of the cases in the top fifth of the forecast with that of the bottom fifth (top minus bottom). The check passes when this difference is above 0.
- Confirm: The slope is positive with t ≥ 2.0 and the top-minus-bottom difference is above 0.
- Reject: The slope is negative with t ≤ -2.0.
- Inconclusive: A slope t between -2.0 and 2.0 is inconclusive. So is t ≥ 2.0 when the top-minus-bottom check fails. The measure needs at least 200 independent 20-bar cases, with at least 40 in the top fifth; with fewer cases the result is inconclusive.
