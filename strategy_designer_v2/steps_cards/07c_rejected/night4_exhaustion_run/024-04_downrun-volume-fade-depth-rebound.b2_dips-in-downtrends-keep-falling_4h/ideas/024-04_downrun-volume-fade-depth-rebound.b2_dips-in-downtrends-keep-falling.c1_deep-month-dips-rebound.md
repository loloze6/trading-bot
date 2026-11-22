---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling
line: 7.c rejected
backtest: 024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: After a falling 4-hour close while the coin's 30-day return is negative, the coin rises over the next six days, and the more negative its 30-day return, the larger the rise.
Consequence: A trader leans long on down bars in coins that have fallen hardest over the month, rather than shorting them.
Why:
- F1: The idea was rejected because its grading runs the wrong way. In the deepest fifth of 30-day returns (mean -36 %), the short side's 18-bar strength is -0.107 (t -2.01, 496 cases) and its 36-bar strength is -0.152 (t -2.78). The three middle fifths (mean 30-day return -20 %, -11 %, -5 %) give +0.097, +0.071 and +0.069 (t 2.44, 1.76, 1.87). The slope of the short-side strength on the 30-day return is positive: 0.43 (t 3.10, 2478 cases) at 18 bars and 0.70 (t 4.86, 2395 cases) at 36 bars. So the more negative the month, the less the coin keeps falling, and at the extreme it rises.
- F2: The same pattern shows on all down-close bars, one per 36-bar grid cell. In the deepest tenth of 30-day returns (mean -39 %), the coin's long-side strength is +0.187 over 6 bars (t 1.86) and +0.129 over 36 bars (t 1.63), with an unusual move of +1.40 % and a total move of +2.22 % over 36 bars (213 cases). Within negative months, the long-side strength falls as the 30-day return rises: slope -0.47 (t -2.25) at 18 bars and -0.62 (t -2.79) at 36 bars, 1036 cases.
