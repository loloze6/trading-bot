---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation
line: 7.d not profitable
backtest: 006-04_upside-squeeze-break-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above the high of its prior 20-day band, price keeps rising beyond the band's top over the next 10 days, and the larger the coin's 20-day return into that break, the further it rises.
Consequence: A break that comes after a strong 20-day climb is worth holding for about ten days, rather than a narrow band's break being worth holding for three.
Why:
- F2: The break itself carries a real rise that outlasts the 3-day window. On the non-overlapping grid, break bars' excess return over the coin's average is +0.0126 over 3 bars (t 2.15, n 244) and +0.064 over 10 bars (t 2.40, n 86), but −0.013 over 20 bars (t −0.41, n 39).
- F3: Holding each coin long for the 10 days after any break bar would have earned a mean daily return of 0.000824, a Sharpe of 0.97 and a Calmar of 0.83. Holding for 1 day earns 0.000117, Sharpe 0.34 and Calmar 0.18. Of the 10-day hold's gain, 0.000552 of 0.000824 is timing, not the market's own rise.
- F4: The excess 10-day return belongs to the break bar itself. It is +0.064 on break bars, but +0.007 on bars 1–5 days after a break and −0.021 on bars 6–10 days after, so entering on the later bars adds nothing.
- F6: The coin's 20-day return into the break does grade the 10-day continuation, with a slope of 0.353 (t 2.36, n 86 grid cases). It does not grade the 3-day continuation (t −0.23).
