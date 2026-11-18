---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g2_ten-day-momentum-continuation
line: 7.d not profitable
backtest: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g2_ten-day-momentum-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 10-day return, and the closer its close sits to the top of its prior 20-day range, the further its price rises over the next 10 days, only while its 30-day return is positive, and the more so the larger that 30-day return.
Consequence: A trader would hold longs sized by strength and range position only inside a rising 30-day trend, and would not short weak coins, which in this data did not fall more than usual.
Why:
- F1: The short side is where the book loses: on 8,255 short bars it lost 0.000244 a bar, and 0.000257 of that came from being short a coin that rises on average (the coin returned +0.000219 a day on those bars). The 8,967 long bars earned 0.000710 a bar, of which 0.000301 was drift and about 0.00041 was timing.
- F2: On the non-overlapping 10-day grid the forecast's information sits only at its top. The top quintile's excess 10-day return was +0.0247 (t 2.50, n=338) and the middle quintile's was -0.0209 (t -2.51). The bottom quintile, which the book shorts hardest, was +0.0006 (t 0.07, n=339), so a weak 10-day return and a close far below the 20-day top did not come before below-average returns.
- F3: Inside a rising 30-day trend the forecast ranks moves well at the top: the top quintile's excess 10-day return was +0.0352 (n=207). In the same trend the bottom quintile was +0.0275 (n=65), so shorting pullbacks inside uptrends lost.
- F4: Longs paid far more inside a rising 30-day trend than inside a falling one: 0.000990 a bar (n=4,602) against 0.000194 (n=2,298). Shorts lost in both trends: -0.000288 in up30 and -0.000335 in down30.
- F7: The deepest falls came from long stretches of the wrong side rather than from coin crashes: XMR w19 fell -35%, XRP w5 -27% and LTC w24 -25%. The correlation between a window's deepest fall and the coin's mean return in that window was only 0.13.
