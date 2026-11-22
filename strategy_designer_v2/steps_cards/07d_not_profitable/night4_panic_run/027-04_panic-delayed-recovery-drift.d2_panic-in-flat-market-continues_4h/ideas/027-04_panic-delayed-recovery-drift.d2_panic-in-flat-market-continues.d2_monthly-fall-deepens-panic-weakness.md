---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-04_panic-delayed-recovery-drift.d2_panic-in-flat-market-continues
line: 7.d not profitable
backtest: 027-04_panic-delayed-recovery-drift.d2_panic-in-flat-market-continues_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: After a 24-hour panic stretch in a coin whose 30-day return before the stretch is negative, the coin's return over the following 14 days is lower than usual, the more so the deeper that 30-day fall.
Consequence: A trader would treat a panic in a coin already falling over the past month as the start of further weakness over the next two weeks, sized by the depth of the monthly fall rather than by the panic's extremity.
Why:
- F3: The short edge lives only where the coin had already fallen over the prior 30 days. In the lowest quartile of the prior 30-day return, cases show an unusual move of +3.98 % (t 2.85, 117 cases) and a total of +1.87 %, about 10 times the cost. In the two middle quartiles they show -0.60 % and -0.69 % (totals -2.56 % and -2.67 %).
- F4: The held bars tell the same story. Bars held after a prior 30-day rise above 13.7 % lose -0.001067 per bar against a market part of -0.000371, while bars held after a 30-day fall below -14 % lose only -0.000007 against -0.000187, a timing gain of about +0.00018 per bar.
- F5: The edge follows bear years, not the panic. The cases' unusual move is +9.4 % in 2018 (t 4.86) and +6.0 % in 2022 (t 3.77), against -7.1 % in 2020 (t -3.26) and -3.1 % in 2024 (t -1.53).
- F6: The forecast is not graded in practice. 532 of 669 cases sit at the -20 cap, with an unusual move of only +0.52 % (t 0.71), against +2.05 % for the 85 cases between -15 and -10, so the supporting check failed (-1.16 %).
