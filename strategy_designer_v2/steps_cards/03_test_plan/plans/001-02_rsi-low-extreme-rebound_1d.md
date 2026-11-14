---
idea: 001-02_rsi-low-extreme-rebound
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: RSI at a low extreme -> adapted: graded as (50 - RSI14) for RSI below 50, with mild readings damped, read "while low" instead of "after reaching".
- Comparison: behaviour after extreme readings vs after neutral readings -> kept: forward returns after the largest positions are compared with those after flat (neutral) bars and with holding.
- Outcome: price rebounds upward over the following bars -> adapted: the long position is held while RSI stays low, with no fixed holding period; it is judged on a 5-bar horizon.
- Verdict transfer: yes: a long that grows as RSI falls profits only if low readings are followed by rises beyond the coin's normal drift, and fails if they are followed by further falls.
Forecast: The forecast is the 14-bar Wilder RSI pullback, (50 - RSI) when RSI is below 50 and 0 otherwise. It is standardised against its own past 60 values, then passed through signed_power with exponent 2 and pivot 10. It is zero whenever RSI is 50 or higher. It is positive (long) when RSI is below 50. It grows with the square of how far RSI sits below 50, so mild readings give a small long and deep oversold readings give a large one, up to the +20 cap. It is never negative.
Config: 001-02_rsi-low-extreme-rebound_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The coin's 5-bar forward return after bars where the forecast is in its top quintile of non-zero values, minus that coin's average 5-bar return over the same window (the hold baseline). Pooled over coins and windows, using non-overlapping 5-bar blocks, before costs.
- Supporting check: The same excess return after top-quintile bars minus the excess after zero-forecast (neutral) bars is positive in at least 2 of the 3 coins.
- Confirm: The pooled mean excess return after top-quintile positions has t >= 2, and the supporting check holds.
- Reject: The pooled mean excess return after top-quintile positions has t <= -2, meaning price keeps falling after low RSI.
- Inconclusive: Any t between -2 and 2, or fewer than 30 non-overlapping top-quintile cases pooled (or fewer than 8 per coin).
