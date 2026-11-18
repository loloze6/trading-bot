---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.g1_high-volatility-one-day-reversal
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.g1_high-volatility-one-day-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 20-day daily volatility stands against its own past year, the more strongly it reverses a vol-scaled 1-day fall over the next 3 days: the larger the day's fall in units of 20-day volatility, the more the coin rises over the next 3 days.
Consequence: A trader can hold the rebound after a high-volatility fall for several days, which cuts the daily turnover whose fees consume most of the one-day edge.
Why:
- F3: Within falls the rebound grows with the size of the fall times its volatility rank (slope 0.0208, t 3.44, n 249), but within rises it does not (slope −0.0017, t −0.43, n 265). Ranked by the 365-bar volatility rank, high-volatility falls give a next-day excess of +0.0172 (t 3.28, n 63) and a 3-day excess of +0.045 (t 2.11, n 17 non-overlapping).
- F4: Fees take most of the edge: gross gain is 0.000333 per bar against fees of 0.000209. Turnover is 0.256 per bar and the position barely persists (autocorrelation −0.04), so fees run from 0.000122 on the smallest moves to 0.000341 on the largest.
