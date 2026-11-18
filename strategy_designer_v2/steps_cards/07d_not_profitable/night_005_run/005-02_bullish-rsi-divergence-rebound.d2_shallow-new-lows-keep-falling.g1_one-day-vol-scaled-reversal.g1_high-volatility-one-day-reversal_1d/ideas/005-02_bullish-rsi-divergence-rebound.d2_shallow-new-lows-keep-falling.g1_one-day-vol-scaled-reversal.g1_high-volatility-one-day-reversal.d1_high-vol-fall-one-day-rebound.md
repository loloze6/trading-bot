---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.g1_high-volatility-one-day-reversal
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.g1_high-volatility-one-day-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 20-day daily volatility stands against its own past year, the more strongly its next 1 day reverses a vol-scaled 1-day move, only after falls: the larger the day's fall in units of 20-day volatility, the more the coin rises over the next 1 day.
Consequence: A trader should buy outsized daily falls in high-volatility periods, sized by the fall and the volatility rank, and should not short outsized rises, since that side earns nothing and pays fees.
Why:
- F1: The fade earns on the long side and not on the short side: bars held long earn 0.000670 per bar before fees and 0.000463 after, while bars held short earn 0.000021 before fees and −0.000195 after, so the short half (2952 of 5842 bars) loses money once fees are paid.
- F2: The next-day rebound after a fall is strongest when volatility is high, and the next day after a rise does not reverse. In the top tercile of the coin's sizing volatility, the next day after a fall gains 0.0060 (t 3.26, n 785). After rises the next day gains +0.0025 in the low tercile (t 2.49), then −0.0016 (t −1.17) and −0.0015 (t −1.01) in the middle and high terciles.
- F3: Within falls the rebound grows with the size of the fall times its volatility rank (slope 0.0208, t 3.44, n 249), but within rises it does not (slope −0.0017, t −0.43, n 265). Ranked by the 365-bar volatility rank, high-volatility falls give a next-day excess of +0.0172 (t 3.28, n 63) and a 3-day excess of +0.045 (t 2.11, n 17 non-overlapping).
- F5: The book is nearly market-neutral and so forgoes the coins' rise. Its mean position is −0.012 and its gain from the market's rise is −0.000015 per day, while holding earns 0.00128 per day. As a result the book's mean daily return is 0.000121 against 0.00128 for holding, its Sharpe is 0.26 against 0.64, and its Calmar is 0.14 against a deepest fall of −21%. It trails holding in 14 of 24 windows.
