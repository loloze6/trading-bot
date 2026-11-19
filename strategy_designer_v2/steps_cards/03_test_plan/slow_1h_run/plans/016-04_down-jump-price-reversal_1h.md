---
idea: 016-04_down-jump-price-reversal
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 1f000a7ba652
---
Fidelity:
- Situation: the coin fell over the past 3 days, and a larger share of that fall came from its 3 biggest hourly losses -> kept: a 72-bar fall gate, sized by the share of the fall carried by the 3 largest hourly losses.
- Comparison: larger share against smaller share of the fall -> kept: the position grows with the share.
- Outcome: the coin wins back more of the fall over the next 3 days (rises) -> kept: the 72-bar forward return, long side.
- Verdict transfer: yes: the forecast is the idea's own share, active only while the coin is down over 72 bars, and is judged on the next 72 bars' rise.
Forecast: A regime gate selects bars where the 72-bar return is below zero. On those bars, the forecast is TopLossesShareOfFallComponent (period 72, k 3, form "share"), standardised over its past 73 values. That is the sum of the 3 largest hourly losses over the net 72-bar fall. It is always positive while the coin is down, so the forecast is long only. It grows continuously with the share, up to the cap of 20. On every other bar the forecast is 0 (flat).
Config: 016-04_down-jump-price-reversal_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: Use bars in regime mean_reversion on the non-overlapping 72-bar grid of each window. For each, take the 72-bar forward return minus that coin's mean 72-bar return over all windows. Regress this pooled over coins on the forecast, and report the slope and its t.
- Supporting check: Rank those fallen cases into forecast terciles. The top tercile's mean excess 72-bar return must be above 0.
- Confirm: The slope is positive with t ≥ 2, and the top tercile's mean excess return is above 0.
- Reject: The slope is negative with t ≤ -2.
- Inconclusive: Any slope with t between -2 and 2 is inconclusive. So is a positive slope with t ≥ 2 whose top tercile's mean excess return is not above 0. At least 300 fallen grid cases are required.
