---
brief: 003_volume-separates-reversal-from-continuation
source-idea: 003-01_thin-volume-rise-reverses.g1_sharp-rises-carry-on
line: 7.g patterns
backtest: 003-01_thin-volume-rise-reverses.g1_sharp-rises-carry-on_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin falls over one day, it rebounds over the next day, and the larger the fall in units of its 20-day volatility of daily returns, the larger the rebound.
Consequence: A sharp down day is a reason to lean long for the next day only, not to follow the fall, with conviction growing with the size of the fall.
Why:
- F1: After a down day, the next day's excess return grows with the size of the fall in 20-day-volatility units: falls beyond 2 units are followed by +0.74% (t 2.32, n 425) and falls of 1 to 2 units by +0.55% (t 4.06, n 1511), against -0.13% (t -1.97, n 4487) after flat days. The slope of the next-day excess return on the downside move is negative in all six coins (t from -1.55 for BTC to -5.82 for XMR, about 2535 bars each), and it holds in both halves of the windows (w1-12: +0.50%, t 3.14, n 963; w13-24: +0.64%, t 3.28, n 973).
- F3: The rebound after a fall does not last 5 days. On the 5-day grid, falls beyond 1 unit give only +0.14% to +0.23% excess (t 0.22 to 0.28, n 405), and after falls beyond 2 units the mean excess turns negative on days 3 and 4 (-0.66% and -0.58%).
