---
line: 7.c rejected
backtest: 024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling_4h
idea tested: 024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling
step 5: rejected
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4358 USD
---
## Findings
- **F1:** The idea was rejected because its grading runs the wrong way. In the deepest fifth of 30-day returns (mean -36 %), the short side's 18-bar strength is -0.107 (t -2.01, 496 cases) and its 36-bar strength is -0.152 (t -2.78). The three middle fifths (mean 30-day return -20 %, -11 %, -5 %) give +0.097, +0.071 and +0.069 (t 2.44, 1.76, 1.87). The slope of the short-side strength on the 30-day return is positive: 0.43 (t 3.10, 2478 cases) at 18 bars and 0.70 (t 4.86, 2395 cases) at 36 bars. So the more negative the month, the less the coin keeps falling, and at the extreme it rises.
- **F2:** The same pattern shows on all down-close bars, one per 36-bar grid cell. In the deepest tenth of 30-day returns (mean -39 %), the coin's long-side strength is +0.187 over 6 bars (t 1.86) and +0.129 over 36 bars (t 1.63), with an unusual move of +1.40 % and a total move of +2.22 % over 36 bars (213 cases). Within negative months, the long-side strength falls as the 30-day return rises: slope -0.47 (t -2.25) at 18 bars and -0.62 (t -2.79) at 36 bars, 1036 cases.
- **F3:** Over the next day, this rebound after deep months is strong in several years and not in others. The 6-bar long strength in the deepest fifth is 0.34 (t 3.63) in 2019, 0.69 (t 2.46) in 2020 and 0.35 (t 2.87) in 2021, but -0.10 in both 2018 and 2022.
- **F4:** Volume sorts the cases against the brief's reading: down streaks on fading volume keep falling, and loud ones bounce. With the last day's volume lowest against its 30-day mean, the short side's 18-bar strength is +0.062 (t 2.32, 1044 cases), an unusual move of 0.61 %. With volume highest, it is -0.031 (t -0.97) over 18 bars and -0.076 (t -2.13) over 6 bars.
- **F5:** The tested idea's move is too small to pay for a trade. Its overall 18-bar strength is 0.026 (t 1.61, 3413 cases), an unusual move of +0.20 % against a 0.19 % trade cost. Its total move is -0.21 %, because the coins' drift works against the short. The book's Sharpe is -0.16.
- **F6:** The short side is not carried by one coin, but it reverses in XMR. Its 18-bar strength is 0.062 in BTC, 0.048 in ETH and 0.021 to 0.029 in the other coins (all t < 1.5), and -0.031 in XMR.

## Ideas
- `024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling.c1_deep-month-dips-rebound` (from F1, F2): After a falling 4-hour close while the coin's 30-day return is negative, the coin rises over the next six days, and the more negative its 30-day return, the larger the rise.
- `024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling.c2_next-day-capitulation-bounce` (from F2, F3): After a falling 4-hour close in a coin whose 30-day return is negative, the coin rises over the next day, and the more negative its 30-day return, the larger the rise.
- `024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling.c3_quiet-down-streaks-continue` (from F4, F1): After an unbroken streak of falling four-hour periods whose loss is large relative to the coin's typical four-hour move over the past 30 days, the coin keeps falling over the next three days, only while the coin's 30-day return is negative. The weaker the coin's volume over the last day against its 30-day average, the larger the further fall.
- `024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling.c4_loud-selling-bounces-back` (from F4): After a falling 4-hour close, the coin rises over the next day, and the larger its volume over the last day against its 30-day average, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
