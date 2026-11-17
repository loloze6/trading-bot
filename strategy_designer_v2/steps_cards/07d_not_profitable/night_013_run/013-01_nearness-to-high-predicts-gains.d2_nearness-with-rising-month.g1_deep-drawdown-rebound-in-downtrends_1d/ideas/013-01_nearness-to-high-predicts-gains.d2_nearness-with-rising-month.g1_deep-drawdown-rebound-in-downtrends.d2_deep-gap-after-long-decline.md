---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 90-day return is negative, the more its 30-day return has fallen and the farther its close sits below its highest close of the past 60 days, the higher its return over the next 7 days.
Consequence: A trader would treat a deep gap below the recent high after a long decline as a graded rebound buy, and would refuse to buy dips after a rising quarter.
Why:
- F3: Inside the regime, the raw depth sorts outcomes the way the idea says. The deepest third has a mean 7-day excess return of -0.15%, the middle third -1.12% and the shallowest third -1.47% (330 cases each). Sorted by the forecast instead, the top third returns -0.13% and the middle third -1.49% (about 409 cases each), with no ordering.
- F4: The depth effect is strongest when the coin's 90-day return is also negative.
- F5: The regime the book trades in loses money and pays fees on it, which is why it trails holding.
