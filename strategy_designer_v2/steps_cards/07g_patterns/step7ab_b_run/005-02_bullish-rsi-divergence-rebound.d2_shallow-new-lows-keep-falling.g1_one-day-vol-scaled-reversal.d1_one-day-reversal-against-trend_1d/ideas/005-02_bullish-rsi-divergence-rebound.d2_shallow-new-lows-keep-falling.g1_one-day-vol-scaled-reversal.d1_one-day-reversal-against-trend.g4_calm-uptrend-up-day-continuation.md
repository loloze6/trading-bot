---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_one-day-reversal-against-trend
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_one-day-reversal-against-trend_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The lower a coin's 20-day volatility against its own past, the more its vol-scaled 1-day rise while its close is above its 50-day average continues over the next 1 day.
Consequence: In a calm uptrend, a trader should follow a strong up day rather than fade it.
Why:
- F3: Among 1-day rises of more than one usual move while the close is above its 50-day average, the correlation between volatility rank and the next-day give-back is 0.14 (t 3.19, 506 cases). In the lowest volatility third those rises keep going up the next day (give-back strength −0.31, t −2.59, 184 cases).
- F1: The tested book's edge grows with the coin's 20-day volatility. On its active days, the next-day directional move net of drift is +0.01 % in the lowest volatility third (t −0.15, 781 cases), +0.38 % in the middle third (t 2.74, 781) and +0.60 % in the top third (t 3.58, 781), which is 5.5 times the 0.11 % round-trip cost. The long side has no edge at all in calm markets: its strength is −0.066 (t −1.07, 437) in the low third against +0.123 (t 2.48, 317) in the high third.
