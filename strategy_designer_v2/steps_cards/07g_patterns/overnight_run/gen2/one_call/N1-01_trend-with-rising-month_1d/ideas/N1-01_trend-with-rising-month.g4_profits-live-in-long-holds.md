---
brief: 002_moving-average-cross-trend-persistence
source-idea: N1-01_trend-with-rising-month
line: 7.g patterns
backtest: N1-01_trend-with-rising-month_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin is above its 200-day average with a rising month, its long positions that survive beyond about ten days carry most of the gain, while those cut within days lose. The persistence shows up only in the multi-week holds that follow.
Consequence: A trader should refuse quick exits on small forecast wiggles and hold until the trend state itself ends.
Why:
- F6: The book's result rests on a few long holds. Trades closed within 10 days lose 2.7% to 4.2% on average (1567 trades), trades held over 30 days gain +98% on average (126 trades), and the top 10% of trades earn 138% of the total net P&L. ZEC alone contributes 6736 of about 11600 summed percent, and LTC is net negative.
- F7: The trend filter adds little forward drift. Non-overlapping forward 20-bar returns are +4.2% in active bars (n=251, t=1.77) against +1.9% and +2.3% in the two flat states (n=331 and 223, t≈1.6). The active excess is negative in 2018 (-15.4%, n=10, t=-2.44) and 2022.
