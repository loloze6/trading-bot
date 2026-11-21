---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_one-day-reversal-against-trend
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_one-day-reversal-against-trend_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day move against its 50-day average, measured in its 20-day usual moves, and the higher its 20-day volatility stands against its own past, the more of that move it gives back over the next 1 day.
Consequence: A trader fading moves that run against the trend should expect the reversal to be paid mainly in volatile markets and should refuse the fade in calm ones.
Why:
- F1: The tested book's edge grows with the coin's 20-day volatility. On its active days, the next-day directional move net of drift is +0.01 % in the lowest volatility third (t −0.15, 781 cases), +0.38 % in the middle third (t 2.74, 781) and +0.60 % in the top third (t 3.58, 781), which is 5.5 times the 0.11 % round-trip cost. The long side has no edge at all in calm markets: its strength is −0.066 (t −1.07, 437) in the low third against +0.123 (t 2.48, 317) in the high third.
- F2: Volatility also decides what follows the moves the idea does not trade. Among 1-day falls of more than one usual move while the close is below its 50-day average, the correlation between the coin's volatility rank and the next-day rebound is 0.18 (t 3.86, 424 cases). In the lowest volatility third those falls keep falling (strength −0.40, t −1.96, 136 cases); in the top third they rebound (+0.18, t 2.07, 154).
- F3: Among 1-day rises of more than one usual move while the close is above its 50-day average, the correlation between volatility rank and the next-day give-back is 0.14 (t 3.19, 506 cases). In the lowest volatility third those rises keep going up the next day (give-back strength −0.31, t −2.59, 184 cases).
