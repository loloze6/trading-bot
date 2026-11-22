---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 8-hour return against its usual 8-hour move over the past 30 days, the more of it the coin gives back over the next 24 hours.
Consequence: A trader leans against a coin's large intraday move for the following day.
Why:
- F8: Large 2-hour and 8-hour moves also reverse over the following day, by more than a trade costs. The top decile of |2h move| is followed by +0.526 % (t 3.3) over the next 24 hours, and the top decile of |8h move| by +0.643 % (t 3.8).
- F3: The one-day reversal is graded and concentrated in the largest moves. By quintile of the 24-hour move scaled by 30-day volatility, the contrarian return rises from −0.118 % (t −1.4) through +0.017 %, +0.287 % (t 3.2) and +0.508 % (t 4.8). Regressing the next-day return on the past-day return gives a negative slope in all 6 coins (−0.068 to −0.126, p ≤ 0.0004).
