---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation
line: 7.d not profitable
backtest: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: While a coin's 60-day return is positive, the higher its 14-day RSI, the more the coin rises over the next 10 days, by more than its usual 10-day move, only while its 14-day RSI is above its midpoint, and the more so the further above it the RSI sits.
Consequence: A trader should take only the long side of this continuation, sized by how far RSI sits above its midpoint, and refuse shorts on soft RSI readings inside an uptrend.
Why:
- F1: Fees, not a missing effect, are what sink the book: across all bars the position earned 0.000647 a day before costs but paid 0.002097 a day in fees, so the book's daily mean is -0.001452 (sd 0.0212, 17,381 coin-days) while holding the coins returned +0.001190 a day.
- F4: The short side does not pay at all: short bars earned -0.000004 per bar gross against 0.000201 per bar in fees. Long bars earned 0.000078 gross against 0.000142 in fees.
- F5: On trending bars with RSI between 45 and 50, the most common short zone (68,893 bars), the book earned 0.000007 per bar gross against 0.000210 in fees, the highest fee of any RSI bin.
- F6: The gain sits where RSI is clearly above its midpoint, and there fees are low. On trending bars it was 0.000180 per bar gross against 0.000073 fees at RSI 55–60, and 0.000321 against 0.000057 at RSI 60–65. On the 240-bar grid, the excess 10-day return was +0.035 at RSI 55–60 (128 cases) and +0.014 at RSI 50–55 (364 cases).
