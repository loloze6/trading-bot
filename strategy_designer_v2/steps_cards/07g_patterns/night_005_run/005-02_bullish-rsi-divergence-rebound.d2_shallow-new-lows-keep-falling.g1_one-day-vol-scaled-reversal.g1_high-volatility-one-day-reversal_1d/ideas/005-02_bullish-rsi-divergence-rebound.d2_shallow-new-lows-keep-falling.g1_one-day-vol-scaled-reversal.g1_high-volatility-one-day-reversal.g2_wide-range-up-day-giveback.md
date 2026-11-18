---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.g1_high-volatility-one-day-reversal
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.g1_high-volatility-one-day-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The wider a coin's rising day's high-low range is in units of its 20-day volatility, the more the coin falls over the next 1 day.
Consequence: A trader can lean short for one day after an up day with an unusually wide range, and refuse to chase such days.
Why:
- F4: A wide high-low range on an up day (range in units of 20-day volatility) is followed by a lower next day. Controlling for z, the range slope on up days is −43.1 bps per unit (t −3.16, n 2445), against +10.6 bps (t 0.96, n 2389) on down days. Over all bars it is −2.6 bps (t −0.45).
- F3: The reversal lasts one day only. On non-overlapping grids the z-slope is +7.35 bps (t 0.69, n 2403) at 2 days, −0.0002 (t −0.13, n 1571) at 3 days and 0.0001 (t 0.05, n 947) at 5 days.
