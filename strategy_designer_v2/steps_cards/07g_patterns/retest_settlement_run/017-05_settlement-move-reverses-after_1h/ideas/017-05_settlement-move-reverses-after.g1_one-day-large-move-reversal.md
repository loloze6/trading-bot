---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 24-hour return against its usual daily move over the past 30 days, the more of it the coin gives back over the next 24 hours.
Consequence: A trader leans against a coin's large one-day move for the following day, and refuses to chase it.
Why:
- F2: After a large one-day move, the coin gives part of it back over the next day. On a non-overlapping 24-hour grid, the top quintile of |24h return| is followed by a drift-removed contrarian 24-hour return of +0.710 % (t 5.8, 3190 cases), and the total move including drift is +0.704 %. That is about 3.7 times the 0.19 % cost of a trade, against 0.05 % per case for the tested idea.
- F3: The one-day reversal is graded and concentrated in the largest moves. By quintile of the 24-hour move scaled by 30-day volatility, the contrarian return rises from −0.118 % (t −1.4) through +0.017 %, +0.287 % (t 3.2) and +0.508 % (t 4.8). Regressing the next-day return on the past-day return gives a negative slope in all 6 coins (−0.068 to −0.126, p ≤ 0.0004).
- F5: The one-day reversal is broad but has faded recently. It is positive in 18 of 24 windows and in all 6 coins (+0.28 % to +0.57 % for the top two quintiles), and it holds after falls (+0.482 %, t 4.3) and after rises (+0.295 %, t 3.0). It is near zero in 2024 (−0.016 %) and 2025 (+0.004 %), against +0.49 % to +0.67 % in 2018, 2019 and 2021–2023.
