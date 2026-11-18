---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.g1_high-volatility-one-day-reversal
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.g1_high-volatility-one-day-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The more a coin's 20-day daily volatility stands above its own average of the past 60 days, the more strongly its next 1 day reverses the day's move measured in units of 20-day volatility: up after large falls, down after large rises.
Consequence: A trader should fade outsized daily moves for one day only while volatility is expanding against its recent norm, sizing the fade by that expansion, and refuse the fade when volatility is at or below its recent norm.
Why:
- F1: The next-day reversal of a vol-scaled daily move appears only when 20-day volatility stands high against its own recent level (20-day vol over its 60-day mean). In the top tercile the slope of next-day excess return on the day's z-score is −51.8 bps per unit (t −3.70, n 987), against +1.4 bps (t 0.12) and −0.5 bps (t −0.04) in the lower two terciles. Pooled, the interaction z × relative-vol is −112.7 bps (t −6.73) and z alone is +104.1 bps (t 5.37), so the reversal grows with the volatility expansion.
- F2: Ranking volatility per coin over the whole record gives the same gradient. The z-slope is −69.7 bps (t −5.82, n 1612) in the top volatility tercile, −0.5 bps (t −0.06) in the middle and +15.3 bps (t 2.15) in the bottom. Next-day excess return after the lowest z quintile is +107.6 bps in high vol against −26.7 bps in low vol. The thresholds in this split are look-ahead, so it is supporting only.
- F3: The reversal lasts one day only. On non-overlapping grids the z-slope is +7.35 bps (t 0.69, n 2403) at 2 days, −0.0002 (t −0.13, n 1571) at 3 days and 0.0001 (t 0.05, n 947) at 5 days.
