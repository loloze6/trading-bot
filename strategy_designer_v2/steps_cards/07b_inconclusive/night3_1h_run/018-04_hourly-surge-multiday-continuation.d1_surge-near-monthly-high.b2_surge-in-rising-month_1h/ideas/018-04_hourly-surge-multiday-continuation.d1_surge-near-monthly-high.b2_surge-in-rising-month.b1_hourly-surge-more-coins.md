---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b2_surge-in-rising-month
line: 7.b inconclusive
backtest: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b2_surge-in-rising-month_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, first reaches several times its 30-day average absolute daily return on the upside, the price keeps rising over the next 10 days by more than the coin's usual 10-day return, only while the coin's 30-day return is positive: the larger the surge in usual daily moves, the larger the rise.
Consequence: A trader would hold an hourly-caught surge for about ten days when it comes inside a rising month, and refuse surges inside a falling month, which carried none of the move.
Why:
- F1: The tested effect points the way the idea predicts but is small and noisy. Over 1,156 cases with 240-hour returns, the mean excess 10-day return after a surge is +0.53 % (t 1.04), with a strength of 0.031 of a usual move. Step 5's own measure is +0.58 % (t 1.15, 1,148 cases). This is below the 0.05 typical of real ideas, and only 46 % of cases end above the coin's drift.
- F5: The effect is spread thinly across coins, which points to too little data rather than one coin carrying it. Five of the six coins are positive over 10 days (+0.3 % to +1.4 %, every t below 1.1), XMR is −1.1 % (t −1.27), and no coin reaches t 2 alone. The test used only 6 of the 19 coins available on hourly bars.
- F7: The move is not too small to pay, but the book's falls are deep. The unusual move per case is 3.0 times the 0.19 % cost of a round trip, and the total move is 10.1 times it. The book's Sharpe is 0.82, above holding by 0.27, but it fails on Calmar (0.62), consistent with the losing years in F4.
