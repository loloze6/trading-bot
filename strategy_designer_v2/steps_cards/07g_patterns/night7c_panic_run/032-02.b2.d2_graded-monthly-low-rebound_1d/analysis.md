---
line: 7.g patterns
backtest: 032-02.b2.d2_graded-monthly-low-rebound_1d
idea tested: 032-02.b2.d2_graded-monthly-low-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4044 USD
---
## Findings
- **F1:** After a large down day (a 1-day return below −1.5 times the coin's 30-day daily standard deviation), the next-day excess return rises with the coin's 30-day volatility. By volatility quintile it is −0.05 % (q0, 55 cases), +0.15 % (q1), +0.87 % (q2, t 1.34), +1.16 % (q3, t 1.88) and +4.88 % (q4, t 2.11, 47 cases on 25 days). In the top two fifths of volatility it is positive in every year (2018 to 2021: +2.6 %, +2.7 %, +5.0 %, +0.6 %) and on all 6 coins (+1.6 % to +6.9 %). It also holds over 3 days on the non-overlapping grid (+3.3 %, t 2.11, 45 cases on 24 days).
- **F2:** A graded signal, the day's return in 30-day standard deviations times minus the coin's volatility rank, orders the next-day excess return. Its top decile earns +0.96 % (t 2.24, 610 cases, 222 days), deciles 0 to 3 earn −0.29 % to −0.37 %, and the middle deciles earn about 0. In the high-volatility half, the most negative return quintile earns +1.01 % (t 2.15, 492 cases) against +0.28 % (t 0.94) in the low-volatility half.
- **F3:** Where the day closes inside its high-low range orders the next day on all bars. Closes in the bottom fifth of the range are followed by +0.61 % excess (t 2.12, 1172 cases, 474 days), and the share falls steadily to −0.39 % (t −1.99) for closes in the top fifth. The signed low-minus-high spread is positive on all 6 coins (XMR +0.98 %, t 4.43; LTC +0.63 %, t 2.67) and in all 4 years. It is about twice as large at high volatility (+0.72 %, t 2.30) as at low volatility (+0.36 %, t 2.06). It is gone over 3 days (+0.07 %, t 0.10).
- **F4:** Inside the tested book's active bars, the range-width part carries the effect. By its tercile the next-day excess is −0.51 % (70 cases), +1.62 % (t 1.50) and +4.45 % (t 2.47, 70 cases, 35 days). Forecast quartiles run −0.41 %, +0.64 %, +2.48 % and +4.75 % (t 2.21).
- **F5:** The monthly-low break itself adds little to a large down day in a decline. A big down day in a 30-day decline without a break earns +0.94 % next day (t 1.45, 114 cases), and one with a break earns +1.42 % (t 1.16, 112 cases). The break bars by window are mixed in sign (w14 −1.03 %, w15 −1.01 %, w16 +6.19 %).

## Ideas
- `032-02.b2.d2.g1_outsized-drop-rebound-in-agitation` (from F1, F2, F5): In a coin whose 30-day daily volatility is high against its own past, a day that falls by a large multiple of that volatility is followed by a rise over the next 1 day. The rise is larger the larger the fall in units of the 30-day volatility, and larger the higher that volatility sits against the coin's past year.
- `032-02.b2.d2.g2_weak-close-next-day-rebound` (from F3): A day that closes near its low within its high-low range is followed by a rise over the next 1 day. The rise is larger the closer the close sits to the low, and larger the wider the coin's 30-day daily volatility.
- `032-02.b2.d2.g3_range-width-weighted-low-rebound` (from F4, F5): In a coin that has fallen over the past 30 days and closes below its prior 30-day low, the rise over the next 1 day is larger the wider its 30-day mean daily high-low range is against its own past year.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
