---
idea: 005-06_bullish-divergence-downtrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: price makes a new low -> adapted: the close sits at or near the bottom of its 20-bar range, used as a regime condition.
- Comparison: RSI makes a higher low than at the prior price low -> adapted: at the new price low, how far RSI(14) is from oversold compared with its own recent past, made graded.
- Outcome: price keeps falling to further lows -> kept: a short position that grows with the divergence.
- Verdict transfer: yes: a short that gains after graded divergences at new lows confirms the idea, and one that loses as strongly rejects it.
Forecast: The forecast is active only on bars where the close is in the bottom 5 percent of its 20-bar close range. That is a Donchian position of -18 or lower, on the -20 to +20 scale. On every other bar it is 0. On active bars it is the equal-weight mean of two components: - The Donchian(20) range position, standardised over 60 bars. Near a new low it is about -20. - The RSI(14) pullback (50 - RSI), standardised over 60 bars. It is positive when RSI is low, and larger the more oversold RSI is. When RSI is as deeply oversold as price, the two cancel and the forecast is near 0 (no divergence). When RSI stays high while price is at its low, the forecast is negative, a short of up to about -10 to -20. The short grows as RSI's low is higher relative to price's low.
Config: 005-06_bullish-divergence-downtrend-continues_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The coin's 5-bar forward return after bars with a negative forecast, times the position, minus the coin's average 5-bar forward return over the same windows. Overlapping bars in one run of active bars count as one case.
- Supporting check: Mean forward return after the larger shorts (forecast <= -5) is lower than after the smaller shorts (-5 < forecast < 0).
- Confirm: Mean excess gain of the short, per non-overlapping case, is positive with t >= 2, before costs.
- Reject: Mean excess gain of the short is negative with t <= -2, meaning price rises after the divergences.
- Inconclusive: Any t between -2 and 2, or fewer than 30 non-overlapping cases pooled over BTC, ETH, BNB and all windows.
