---
idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d1_settlement-shock-extending-crowded-run
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: the 00:00 UTC hour's return runs the same way as the previous 23 hours' return -> adapted: "after the settlement hour" is made "while it is the bar of that hour", as a regime rule on the hour and on both returns' signs.
- Comparison: that hour's return relative to its 24-hour volatility -> kept: the hour's return divided by the standard deviation of the last 24 one-hour returns, graded.
- Outcome: the next 24 hours run opposite to the hour's move, more so the larger it is -> kept: a fade sized by the scaled move, held 24 bars.
- Verdict transfer: yes: the test bets only on the aligned settlement-hour bars, fades them in proportion to the scaled move, and judges the next 24 hours.
Forecast: The regime detector selects `mean_reversion` only on the bar stamped 00:00 UTC, which is the one whose coming bar starts at 01:00. It also needs that bar's one-hour return and the return of the 23 hours before it (close[t-1]/close[t-24]-1) to have the same sign. On every other bar the regime is `unknown` and the forecast is 0. In `mean_reversion` the forecast has three steps: - It starts from the hour's return divided by the standard deviation of the last 24 one-hour returns (VolatilityScaledReturnComponent, period 1, vol_period 24). - That value is standardised against its past 60 values (target 10, cap 20). - It is then negated. So the forecast is short after an aligned up-hour and long after an aligned down-hour. Its size grows linearly with the scaled move and is near 0 for a tiny hour. Each bet is held 24 bars.
Config: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d1_settlement-shock-extending-crowded-run_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: On the case bars (non-zero forecast, at most one per coin-day), the least-squares slope of the coin's 24-bar forward return from the case bar's close on the forecast. The return is taken minus the coin's mean 24-bar return over all windows. The slope is pooled over coins and windows, before costs, with its t.
- Supporting check: The mean over cases of sign(forecast) x that excess 24-bar return is above 0.
- Confirm: The slope is positive with t >= 2 on at least 300 cases, and the supporting check passes.
- Reject: The slope is negative with t <= -2 on at least 300 cases.
- Inconclusive: A t between -2 and 2, a positive slope whose supporting check fails, or fewer than 300 cases.
