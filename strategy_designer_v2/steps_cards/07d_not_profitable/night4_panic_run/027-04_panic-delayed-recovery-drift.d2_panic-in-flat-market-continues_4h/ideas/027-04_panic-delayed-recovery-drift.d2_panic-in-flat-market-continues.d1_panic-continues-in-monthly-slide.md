---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-04_panic-delayed-recovery-drift.d2_panic-in-flat-market-continues
line: 7.d not profitable
backtest: 027-04_panic-delayed-recovery-drift.d2_panic-in-flat-market-continues_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: After a 24-hour panic stretch, the coin's return from one day after the stretch ends to 14 days after it is lower than usual, the more so the more extreme the panic, while the coin's 90-day return before the stretch is close to flat, only while the coin's 30-day return before the stretch is negative, and the more so the deeper that 30-day fall.
Consequence: A trader would short a coin after a panic only when it was already sliding over the past month, and would refuse to short a panic that hits a coin that had been flat or rising over the month.
Why:
- F1: The book loses because it is short a coin that rises. Its gain per bar is -0.000153, and -0.000157 of that is the market part (being short about 58 % of bars into the coins' own rise), while timing adds only +0.000004. Its daily returns correlate -0.66 with the coins', and in every one of its eight worst windows the coins rose, for example w21 with the book at -0.86 % a day and the coins at +0.57 %.
- F2: Per case, the unusual move in the short direction (+1.04 %, t 1.52, 669 cases) is smaller than the coin's normal drift against the short (about -2 %). The total move is therefore -0.96 % per case, -4.0 times the 0.19 % cost of a trade, so no change of holding or sizing can make this book pay.
- F3: The short edge lives only where the coin had already fallen over the prior 30 days. In the lowest quartile of the prior 30-day return, cases show an unusual move of +3.98 % (t 2.85, 117 cases) and a total of +1.87 %, about 10 times the cost. In the two middle quartiles they show -0.60 % and -0.69 % (totals -2.56 % and -2.67 %).
- F4: The held bars tell the same story. Bars held after a prior 30-day rise above 13.7 % lose -0.001067 per bar against a market part of -0.000371, while bars held after a 30-day fall below -14 % lose only -0.000007 against -0.000187, a timing gain of about +0.00018 per bar.
- F5: The edge follows bear years, not the panic. The cases' unusual move is +9.4 % in 2018 (t 4.86) and +6.0 % in 2022 (t 3.77), against -7.1 % in 2020 (t -3.26) and -3.1 % in 2024 (t -1.53).
