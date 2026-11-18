---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-03_lower-wick-flush-recovery
line: 7.d not profitable
backtest: 012-03_lower-wick-flush-recovery_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Among bars that fall sharply on a volume burst, the longer the lower wick below the close, as a share of the bar's high-to-low range, the larger the price rise over the next 3 days, only while the coin's 20-day return is negative, and the more so the deeper that 20-day fall.
Consequence: A trader buys wick flushes only after the coin has already fallen over the past 20 days, sizing up the deeper that fall, and refuses flushes in flat or rising markets.
Why:
- F5: The book's result rests on one window. Window w3 alone sums to -0.246 in daily book returns, against -0.074 for the next worst (w1), and the Sharpe stays at -0.21 with one window left out.
- F6: The rebound grows with the depth of the coin's prior fall. Flush bars in the lowest quarter of 20-day return (mean -32 %) rose 4.30 % the next day (t 2.92, n 49) and 3.69 % over 3 days (t 2.22, n 49). The other quarters rose between -0.28 % and 0.48 % the next day, all with |t| below 0.6.
