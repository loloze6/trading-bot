---
idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the coin's fall over the 24 hours up to the 20:00 UTC close -> kept: a regime on the hour selects the bar closing at 20:00, and a negated 24-bar return, clipped at 0, measures the fall.
- Comparison: larger falls against smaller falls ("the more ... the more") -> kept: the forecast grows with the depth of the fall.
- Outcome: the coin rises over the next 24 hours, more after deeper falls -> adapted: the holding period is dropped (the position lasts one bar), and the 24-bar forward return is measured from the record.
- Verdict transfer: yes: the 20:00 forecast and the 24-bar forward closes are both recorded, so the relation is measured exactly as the idea states it.
Forecast: The regime is active only on the hourly bar that closes at 20:00 UTC, where the coming bar's hour is 20. On that bar the forecast is the coin's 24-bar percent return, standardised over its last 60 hourly values, negated and clipped at 0. It is positive and grows with the depth of the 24-hour fall, and it is 0 when the coin rose. On every other bar the forecast is 0 (flat).
Config: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: The sample is the regime bars (the 20:00 closes, one per day, so the samples do not overlap), pooled over all coins and windows. Each case's excess return is close[t+24]/close[t]-1, inside the same window, minus that coin's mean 24-bar return over all windows (holding the coin). The measure is the OLS slope of the excess return on the bar's `forecast`, with its t-statistic.
- Supporting check: On the bars with forecast > 0, the mean excess 24-bar return is above 0.
- Confirm: The slope's t is 2 or more AND the mean excess return on forecast > 0 bars is above 0.
- Reject: The slope's t is -2 or less.
- Inconclusive: Any other result, including a t between -2 and 2, is inconclusive. A slope with t ≥ 2 but a mean excess return on forecast > 0 bars that is not above 0 is also inconclusive. The test needs at least 2000 regime bars with a full 24-bar forward return and at least 500 of them with forecast > 0; with fewer, the result is inconclusive.
