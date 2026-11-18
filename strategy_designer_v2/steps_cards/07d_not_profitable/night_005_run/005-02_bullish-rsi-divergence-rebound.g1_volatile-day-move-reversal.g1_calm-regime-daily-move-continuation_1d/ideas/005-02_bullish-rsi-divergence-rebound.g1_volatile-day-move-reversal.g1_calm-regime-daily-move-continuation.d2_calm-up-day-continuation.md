---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 20-day volatility is low relative to its last 100 days, a large one-day rise continues upward over the next 3 to 7 days. The larger the day's rise relative to the coin's 60-day mean absolute daily move, and the lower the 20-day volatility rank, the larger the further rise.
Consequence: In calm stretches a sharp up day is a reason to follow it, while a sharp down day gives no reason to short.
Why:
- F5: The book's gain sits on the long side. Long bars gain 0.000873 per bar and short bars lose 0.000134. After top-quintile up days the coin's raw 5-day return is +0.0225 (n = 625); after top-quintile down days it is +0.001 (n = 545), so it does not fall.
- F3: The continuation the verdict confirmed is not on the day the book holds. After top-quintile bars, the signed excess return is 0.00033 on day 1 (t = 0.29, n = 1170). It is 0.0042 on day 2 (t = 3.81), 0.0021 on day 3 (t = 1.96) and 0.0028 on day 5 (t = 2.43). So the book trades the one day without the effect and is out for the days that carry it.
