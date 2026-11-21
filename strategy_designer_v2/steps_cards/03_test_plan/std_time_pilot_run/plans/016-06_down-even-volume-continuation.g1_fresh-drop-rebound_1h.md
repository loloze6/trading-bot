---
idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: the coin has fallen over the past 3 days, with a fall over the last 1 day -> adapted: "has fallen over 3 days" is kept as an on/off regime condition, because the idea is itself a condition; the size of the 1-day fall is kept as a graded measure.
- Comparison: a larger 1-day fall against a smaller one -> kept: the position grows with the size of the 24-bar fall.
- Outcome: the coin rises more over the next 3 days -> kept: 72-bar forward return, long side.
- Verdict transfer: yes: the test measures how the 72-bar rise grows with the 24-bar fall, only while the 72-bar return is negative, as the idea states.
Forecast: A regime rule checks the 72-bar return (PriceEvolutionComponent, period 72). When it is below 0, the bar is mean_reversion; otherwise the bar is unknown, which is flat. In mean_reversion, the forecast is the 24-bar return (PriceEvolutionComponent, period 24), standardised over its 60 prior values (min_periods 20), negated, then clipped at 0. It is positive and grows with the size of the last day's fall. It is zero when the last day rose or when the 3-day return is not negative. It is never short.
Config: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: Use the grid of bars at positions 0, 72, 144, ... of each window, keeping only bars whose regime is mean_reversion. On those bars, regress the coin's 72-bar forward return minus that coin's mean 72-bar return over all windows on the forecast. Pool coins and windows, and report the slope's t.
- Supporting check: On the same grid bars, the forecast-weighted mean of the excess 72-bar return is above 0.
- Confirm: The slope's t is 2 or more and the supporting check passes.
- Reject: The slope's t is -2 or less.
- Inconclusive: Any t between -2 and 2, or t of 2 or more with the check failing. At least 200 grid bars in mean_reversion are required, of which at least 100 have a forecast above 0; fewer cases is inconclusive.
