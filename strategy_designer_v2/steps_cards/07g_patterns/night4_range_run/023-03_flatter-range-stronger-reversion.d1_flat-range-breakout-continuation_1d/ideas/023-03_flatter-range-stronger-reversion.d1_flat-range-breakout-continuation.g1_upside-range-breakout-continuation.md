---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's close sits to the top of its 30-day closing range, the larger its rise over the next 5 days; a close near the bottom of the range is followed by little further fall.
Consequence: The long side of a 30-day range breakout is worth taking, and fading it should be refused, while shorting a close near the range low should be refused.
Why:
- F2: The book's gain comes from its long side. 3810 long trades earned +3.56 % each after fees, while 4832 short trades lost −0.60 % each. On the grid, the top fifth of range position (mean 0.97 of the 30-day range) is followed by +1.39 % above drift over 5 days (t 2.36, 511 cases), while the bottom fifth (mean 0.05) is followed by only −0.37 % (t −0.63).
- F3: Flatness does not scale the move as the idea says. The least flat fifth of 30-day windows, the one-way months, is followed by +1.52 % above drift (t 2.78, 511 cases), which is the largest of the five fifths. The flattest fifth is followed by −0.47 % (t −1.13). By 30-day net move against the range, the top fifth is followed by +1.06 % (t 1.88) and the second-lowest fifth by −1.32 % (t −3.13), which reads as continuation of the month's trend.
