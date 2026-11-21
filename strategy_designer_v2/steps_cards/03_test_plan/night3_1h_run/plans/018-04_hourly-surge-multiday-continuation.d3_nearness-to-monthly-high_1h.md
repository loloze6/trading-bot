---
idea: 018-04_hourly-surge-multiday-continuation.d3_nearness-to-monthly-high
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 1efb53e47d25
---
Fidelity:
- Situation: how close the hourly close stands to its 30-day high -> kept
- Comparison: the coin's usual 5-day return -> kept
- Outcome: the coin rises more over the next 5 days, the closer it is to the high -> kept
- Verdict transfer: yes: the forecast is the graded nearness to the 720-bar closing high, and the test compares the next 120-bar return with the coin's usual 120-bar return.
Forecast: The only indicator is the nearness of the close to its highest close of the last 720 hourly bars (30 days), with the current bar included. It is read as a proximity 1 / (1 + D), where D is the percent distance below that high. The value is 1 at a new high and falls smoothly toward 0 the further the close falls back. `standardise` puts it on the scale of its own past 500 values, so the forecast is about +10 at the coin's usual nearness, up to +20 at or very near the high, and close to 0 deep inside a decline. It is never negative, so the position is long and grows with nearness to the month's high. It is ungated and active on every bar.
Config: 018-04_hourly-surge-multiday-continuation.d3_nearness-to-monthly-high_1h_config.json
Criterion:
- Horizon: 120 bars
- Main measure: Cases are taken on the non-overlapping 120-bar grid of each window, pooled over all coins. For each case, the excess return is the coin's 120-bar forward return minus that coin's mean 120-bar return over all its windows. The measure is the mean excess return of cases in the top third of the forecast minus the mean of cases in the bottom third, tested with Welch's t.
- Supporting check: The same top-minus-bottom difference is positive on at least 4 of the 6 coins.
- Confirm: The difference is positive with Welch t >= 2, and the supporting check passes.
- Reject: The difference is negative with Welch t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A positive t >= 2 that fails the coin check is also inconclusive. The test needs at least 200 cases in each of the top and bottom thirds; with fewer, it is inconclusive.
