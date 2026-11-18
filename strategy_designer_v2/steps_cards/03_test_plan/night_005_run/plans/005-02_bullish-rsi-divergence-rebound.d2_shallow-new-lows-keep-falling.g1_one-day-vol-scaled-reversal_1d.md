---
idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 791f9c660ae8
---
Fidelity:
- Situation: a 1-day fall scaled by 20-day volatility, with the close near the day's low; a vol-scaled 1-day rise -> kept
- Comparison: the coin's own 20-day daily volatility -> kept
- Outcome: the coin rises over the next 1 day after the fall, and gives back over the next 1 day after the rise -> kept
- Verdict transfer: yes: every part is measured as the idea states it.
Forecast: The forecast is the equal-weight mean of two parts. - Long part (FallCloseLocationComponent, vol_period 20): the size of today's fall in 20-day usual moves, times how near the close is to the day's low. It is 0 on up days and is standardised over 60 bars. - Short part (VolatilityScaledReturnComponent, period 1, vol_period 20): today's return in 20-day usual moves. It is standardised over 60 bars, clipped at 0 so only rises count, then negated. On a down day the forecast is positive and grows with the depth of the fall and the nearness of the close to the low. On an up day it is negative and grows with the size of the vol-scaled rise. It is near zero on small moves. The forecast is re-set every bar, so each position lasts one day.
Config: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The mean over all bars of forecast[t] x (close[t+1]/close[t] - 1 - the coin's mean daily return over all windows), pooled across coins and windows, with its t of the mean. The 1-bar samples do not overlap. This is the gain before costs, beyond holding the coin, and it grows with the size of the position.
- Supporting check: The mean next-day excess return on bars with forecast > 0, minus that on bars with forecast < 0, is above zero.
- Confirm: The main measure has t >= 2 and the supporting check is positive.
- Reject: The main measure has t <= -2.
- Inconclusive: Any t between -2 and 2, or t >= 2 with a check that is not positive. A result needs at least 1000 bars with a non-zero forecast and at least 300 on each side; fewer is inconclusive.
