---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's daily close comes to a new 30-day closing high, measured by how many of the past 30 days' closes it exceeds, the more the coin rises over the next 10 days.
Consequence: A trader should lean long on a coin closing at or near a new monthly high, and should not treat a close only somewhat above the month's middle as the same signal.
Why:
- F5: Within the upper range, the response is not graded. Only the close at the 30-day closing high stands out, with +4.69 % excess over 10 days (t 2.3, 137 cases). Even that rests mainly on XRP (+22.9 %, 18 cases), while the 0.7 to 0.9 band of the range is followed by -1.75 % (t -2.1, 210).
- F4: The tested idea's gain sits in only part of the book: forecast>0 grid cases beat forecast-0 cases by 3.4 points in ETH, 2.0 in XRP and 4.0 in ZEC but by about 0 in LTC (-0.09 % vs +0.08 %) and XMR (-0.01 % vs +0.01 %), and the book's best 2 % of days carry 141 % of its mean daily gain.
