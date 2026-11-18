---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation.g1_calm-up-day-continuation
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation.g1_calm-up-day-continuation_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: In BTC or ETH, when the 20-day volatility is low relative to its last 100 days, a large up day is followed by a further rise that builds over the next 5 days, mostly in the second to fifth days after it rather than on the next day. The larger the day's gain relative to the coin's 60-day mean absolute daily move, and the lower the volatility rank, the larger that rise over the whole 5 days.
Consequence: A trader should hold a calm-regime sharp up day's long through the following five days instead of only overnight. This lets the trade capture the delayed rise and cut the round-trip fees that eat the one-day trades.
Why:
- F1: The book holds the coin almost only on the signal day: the mean position is 0.330 on the bar the forecast is positive, then 0.005 one day after and 0.006 two days after. It therefore collects the next day's move alone, a mean gain of 0.000893 on 2,817 signal bars.
- F2: The forecast's rise comes mostly after the first day. On the non-overlapping 5-bar grid, bars with forecast in (2, 8] gained 0.0045 on day 1 but 0.0252 from day 1 to day 5 (61 cases). Bars with forecast in (8, 20] gained 0.0040 against 0.0150 (144 cases), and their 10-day returns were 0.039 and 0.032. The book holds the coin during none of those later days.
- F3: In-and-out daily trading loses to fees. Of 1,263 trades, 774 last at most 1.5 days, and they average −1.08% net (−835% summed). Trades of 1.5–6.5 days average +4.2% to +7.7% net. Summed per-bar fees (0.61 BTC, 0.55 ETH) take about 45% of summed gross gains (1.31, 1.17).
- F4: As a result, the book's mean daily return is 0.000231 against the coin's 0.001275. Its Sharpe is 0.285 below holding's, and its Calmar is 0.131, with per-coin chained deepest falls of −48% (BTC) and −52% (ETH). The book is in the market only 31% of bars, at a mean position of 0.52 when in.
- F5: The effect itself is graded in the raw situation. Across quintiles of the positive raw component on the grid, the 5-day forward return rises steadily: −0.021, −0.004, 0.009, 0.015, 0.025 (about 105 cases each). The 10-day return in the top quintile is 0.040.
