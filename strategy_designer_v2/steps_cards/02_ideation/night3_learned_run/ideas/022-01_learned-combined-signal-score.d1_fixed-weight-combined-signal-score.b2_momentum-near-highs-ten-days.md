---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score
line: 7.b inconclusive
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 28-day return plus its closeness to its 90-day high, the higher its return over the next 10 days.
Consequence: A trader would lean long a coin that has risen over four weeks and stands near its three-month high, more so the stronger both are, and hold it for about ten days.
Why:
- F3: At horizons other than 5 days the same forecast clears t 2: t 5.05 at 1 day (17380 cases), 3.45 at 2 days, 3.23 at 3 days, 2.81 at 10 days (1691 cases) and 2.33 at 20 days (827 cases).
- F4: Of the four signals, the 28-day return carries the score at 2 to 10 days (t 1.95 to 2.68), and closeness to the 90-day high adds a little (t 0.83 to 1.65). Together they reach t 2.24 to 2.72 from 2 to 10 days. The short reversal shows only at 1 day (t 5.10; −1.47 at 5 days), and minus volatility shows at no horizon (t −0.55 to −0.00).
- F6: Size against cost: the unusual move is +0.96 % per case over 5 days, a strength of 0.082 and 5.0 times the 0.19 % round trip. Over 10 days it is +0.83 % in the signal's direction, against a usual move of 15.9 %. The book's Sharpe is 0.94, 0.38 above holding, and it fails only on mean daily return (0.00029) and Calmar (0.75).
