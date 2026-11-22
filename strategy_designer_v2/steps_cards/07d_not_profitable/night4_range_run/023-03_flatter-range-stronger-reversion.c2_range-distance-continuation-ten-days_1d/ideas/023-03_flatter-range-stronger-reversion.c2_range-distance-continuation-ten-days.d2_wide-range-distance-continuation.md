---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days
line: 7.d not profitable
backtest: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The farther a coin's daily close sits from the middle of its 30-day closing range, the more the coin keeps moving in that direction over the next 10 days, up from above the middle and down from below it, the more so the wider that 30-day range is against its middle.
Consequence: A trader should lean with moves away from the middle of a wide monthly range and give little weight to the same move inside a tight range.
Why:
- F4: In narrow 30-day ranges the effect is absent on both sides: unusual move -0.39 % above the middle (213 cases) and -0.47 % below it (207 cases). It shows in wider ranges: +2.88 % above the middle in mid-width ranges (t 2.24, 206 cases), and -2.24 % below it in wide ranges (t -2.20, 234 cases). Only there does the raw 10-day return turn negative below the middle (-0.98 %).
- F5: The signed unusual move grows with the trend of the past 30 days: +0.57 % (t 0.95) in the flattest third, +1.21 % in the middle third and +1.49 % in the most trending third, each with about 420 cases.
- F2: Below the middle the coin's raw 10-day return is still positive: +0.65 % at the range bottom (position -1 to -0.6, 331 non-overlapping cases) and +0.13 % at -0.6 to -0.2 (237 cases). Its unusual move there is negative but not reliable (-0.59 %, t -0.79; -1.10 %, t -1.34), so shorts pay the coin's normal rise (+0.12 % a day held) without a matching gain from timing.
