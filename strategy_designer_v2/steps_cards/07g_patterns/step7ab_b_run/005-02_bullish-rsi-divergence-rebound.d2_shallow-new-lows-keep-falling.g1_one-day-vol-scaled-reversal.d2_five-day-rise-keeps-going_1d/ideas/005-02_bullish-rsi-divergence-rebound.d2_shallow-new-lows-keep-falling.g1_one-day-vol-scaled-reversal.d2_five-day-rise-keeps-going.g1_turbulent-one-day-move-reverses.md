---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_five-day-rise-keeps-going
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_five-day-rise-keeps-going_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 20-day daily volatility is high against its own usual level, the larger its last day's return relative to that volatility, the more of it the coin gives back over the next day, with a large one-day fall followed by a rebound and a large one-day rise by a decline.
Consequence: In a turbulent stretch a trader should lean against the last day's vol-scaled move for one day rather than chase it, and refuse to follow a sharp one-day move.
Why:
- F1: When a coin's 20-day volatility is above its own median, a large one-day rise is followed by a fall the next day: the slope of the next day's unusual return on the day's return in units of 20-day volatility is −0.118 (t −5.0, 2,420 one-day cases). With volatility below its median the slope is +0.027 (t +1.8, 2,414 cases). The difference between the two slopes has a t of about −5.1, which stands out even after the many angles looked at.
- F2: Over all bars, the one-day reversal is graded. The day after the bottom fifth of vol-scaled one-day returns earns an unusual +0.21 % (raw +0.34 %). After the top two fifths it earns −0.23 % and −0.13 % (raw −0.10 % and −0.00 %). The pooled slope t is −2.86 on 4,834 cases, and both coins show it (BTC t −1.6, ETH t −2.4).
- F3: The one-day reversal is also stronger when 20-day volatility is high against 60-day volatility (t −3.6, 3,382 cases; t +0.4 otherwise). It is stronger when the coin's 60-day return is negative (t −3.3, 3,279 cases; t −0.4 when positive). Both conditions overlap with high volatility (F1).
