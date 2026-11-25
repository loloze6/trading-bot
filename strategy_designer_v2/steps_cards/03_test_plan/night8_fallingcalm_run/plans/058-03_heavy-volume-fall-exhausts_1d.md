---
idea: 058-03_heavy-volume-fall-exhausts
brief: 058_quiet-volume-calm-decline-continues
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 27e35f604dd2
---
Fidelity:
- Situation: in a falling, calm market, a coin that has fallen over its last 30 days, with its 30-day volume set against its past-year average -> kept: the profile is added by code; "fallen over 30 days" is a regime (30-day return below 0); volume is a 30-bar against 365-bar mean ratio
- Comparison: the coin's own average volume over the past year -> kept
- Outcome: the heavier the volume, the less the coin falls over the next 5 days -> kept: 5-bar forward return, higher for heavier volume
- Verdict transfer: yes: the test measures whether, inside the situation, heavier relative volume is followed by a higher 5-day return than quieter volume, and the reverse.
Forecast: The forecast is active only on bars where the coin's 30-day return is below 0 (regime `mean_reversion`). Every other bar is flat. The idea's profile (falling calm) is added by code. Inside the regime, the forecast is ln(mean volume of the last 30 bars / mean volume of the last 365 bars), standardised over its last 365 values (min 91). The forecast is positive and grows when recent volume is heavier than the year's average (less fall ahead, so relatively long). It is negative and grows in size when volume is thinner (the fall carries on, so short). It is 0 when recent volume equals the average.
Config: 058-03_heavy-volume-fall-exhausts_1d_config.json
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The measure uses non-overlapping 5-bar grid cells of each window, on bars in regime `mean_reversion` with a forecast not 0. It is the mean 5-bar forward return of the heavy-volume cases (forecast > 0) minus that of the quiet-volume cases (forecast < 0), with Welch's t. The difference cancels the coin's own drift.
- Supporting check: none
- Confirm: The difference (heavy minus quiet) is positive with Welch t ≥ 2.
- Reject: The difference is negative with Welch t ≤ -2: heavy-volume declines fall more than quiet ones.
- Inconclusive: Any t between -2 and 2 is inconclusive. The result is also inconclusive with fewer than 30 cases in either group.
