---
idea: 001-01_rsi-high-extreme-reversal
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Forecast: Use the 14-bar Wilder RSI on daily closes, taken from RSIPullbackComponent (period 14), which outputs (50 − RSI) × 0.4. Standardise it against the mean absolute value of its own previous 60 readings (min_periods 20, target 10, cap 20). Clip it at a maximum of 0, so only the overbought side is kept: zero whenever RSI ≤ 50, negative when RSI > 50. Then apply signed_power with exponent 2 and pivot 10. This damps mild readings towards 0 (−5 becomes −2.5) and amplifies extreme ones (−15 becomes −22.5, and the combined forecast is clipped at −20). The forecast is therefore never positive. It is 0 when RSI is at or below 50, and it shorts the coin more and more strongly the further RSI sits above 50, measured against the coin's own recent RSI excursions. It runs on every bar, with no regime gate.
Config: 001-01_rsi-high-extreme-reversal_config.json
Confirm: Horizon is 5 bars. Take the bars where the forecast is ≤ −10, keeping one entry per non-overlapping 5-bar block. Over all 3 coins and 6 windows, the coin's 5-bar forward close-to-close return after those bars is at least 1.0 percentage point below the coin's unconditional mean 5-bar return over the same windows (buy-and-hold). The t-statistic on the non-overlapping returns must be ≤ −2, and the difference must be negative in at least 2 of the 3 coins. Supporting check: the strategy's before-cost return, pooled across windows, is positive in at least 2 of the 3 coins.
Reject: Pooled across coins and windows, the mean 5-bar forward return after forecast ≤ −10 bars is equal to or above the unconditional mean 5-bar return, or the difference is ≥ 0 in at least 2 of the 3 coins.
Inconclusive: The pooled difference is negative but smaller than 1.0 percentage point, or the t-statistic is between −2 and 0. Also inconclusive: fewer than 30 non-overlapping qualifying blocks in the pooled sample.
Deviation: The idea says "after the RSI reaches a high extreme". The config tests "while the RSI is above 50", with a short sized by how far above 50 it is. Mild readings take small damped shorts rather than none. The extreme is judged against the coin's last 60 RSI readings, not against a fixed level such as 70. The config holds the position only while the reading stays high; it does not hold it for a set number of bars after the extreme.
