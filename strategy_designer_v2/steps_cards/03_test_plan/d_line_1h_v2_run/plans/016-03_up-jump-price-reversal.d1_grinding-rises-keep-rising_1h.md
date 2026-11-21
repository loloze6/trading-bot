---
idea: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a coin has risen over the past 3 days, and a smaller share of that rise came from its few biggest hourly gains (a grind) -> adapted: graded as 1 minus the top-3 hourly gains' share of the 72-bar rise, and 0 when the coin did not rise.
- Comparison: grinding rises against jump-made rises -> kept: the forecast ranks rises by how little of them the top-3 hourly gains carry.
- Outcome: the more grinding the rise, the more the coin keeps rising over the next 3 days -> kept: the long position is sized by grind, and the forward return is measured over 72 bars.
- Verdict transfer: yes: the forecast is the idea's own evenness-of-rise measure, applied to past 3-day rises and sized by it, and it is judged on the next 3 days.
Forecast: The forecast uses TopGainsShareOfRiseComponent with period 72 (3 days of 1h bars), k 3 (the few biggest hourly gains) and form "residual". Its value is 1 minus (the sum of the 3 largest hourly gains / the net 72-bar rise), capped to 0..1 when the coin rose. It is 0 when the coin did not rise over 72 bars. Standardise (window 72, min_periods 20) puts it on the forecast scale. The forecast is always zero or positive, so the book is long only and never short. It is 0 after no rise or after a rise made entirely by its 3 biggest hours. It grows continuously as the rise spreads over many small hourly steps, up to the cap of 20.
Config: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: Use the non-overlapping 72-bar grid of each coin-window, keeping only the grid bars where close[t]/close[t-72]-1 > 0 (recomputed from closes). Take the next-72-bar return minus the coin's mean 72-bar return over all windows. Regress that excess return, pooled over coins, on the forecast and on the past 72-bar return. The measure is the t of the forecast's coefficient: the grind effect beyond the rise's size.
- Supporting check: none
- Confirm: The forecast coefficient is positive with t >= 2.
- Reject: The forecast coefficient is negative with t <= -2. In that case grinding rises continue less than jump-made rises of the same size.
- Inconclusive: Any t between -2 and +2 is inconclusive. So is any result from fewer than 300 rising grid cases pooled over the coins.
