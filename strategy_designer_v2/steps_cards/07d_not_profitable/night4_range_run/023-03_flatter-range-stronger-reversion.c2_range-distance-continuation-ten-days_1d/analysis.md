---
line: 7.d not profitable
backtest: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days_1d
idea tested: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3471 USD
---
## Findings
- **F1:** The short side loses the book's money: on daily book returns the long-only part earns +0.000695 a day (Sharpe 0.92, deepest fall -31 %, Calmar 0.77), while the short-only part loses -0.000191 a day (Sharpe -0.26, deepest fall -72 %). LONG trades net +7.52 % on average over 2678 trades, and SHORT trades net -2.02 % over 3475.
- **F2:** Below the middle the coin's raw 10-day return is still positive: +0.65 % at the range bottom (position -1 to -0.6, 331 non-overlapping cases) and +0.13 % at -0.6 to -0.2 (237 cases). Its unusual move there is negative but not reliable (-0.59 %, t -0.79; -1.10 %, t -1.34), so shorts pay the coin's normal rise (+0.12 % a day held) without a matching gain from timing.
- **F3:** The effect sits at the top of the range. Near the 30-day high (position 0.6 to 1) the unusual 10-day move is +1.75 % (t 1.80, 356 cases; raw +3.00 %). By forecast quintile only the top one is clearly positive (+2.43 %, t 2.15, 338 cases), and the others run from -0.13 % to -1.54 %.
- **F4:** In narrow 30-day ranges the effect is absent on both sides: unusual move -0.39 % above the middle (213 cases) and -0.47 % below it (207 cases). It shows in wider ranges: +2.88 % above the middle in mid-width ranges (t 2.24, 206 cases), and -2.24 % below it in wide ranges (t -2.20, 234 cases). Only there does the raw 10-day return turn negative below the middle (-0.98 %).
- **F5:** The signed unusual move grows with the trend of the past 30 days: +0.57 % (t 0.95) in the flattest third, +1.21 % in the middle third and +1.49 % in the most trending third, each with about 420 cases.
- **F6:** The failing measures follow from F1 and F2. The book's mean daily return of 0.000438 is below holding's 0.0012 a day, and the deepest fall of the chained book is -50.7 %, over 236 days from w19 to w21. In the windows where the coin rose, such as w11 (+0.0126 a day) and w20, the short part lost -0.0024 and -0.0021 a day.

## Ideas
- `023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only` (from F1, F2, F3, F6): The farther a coin's daily close sits above the middle of its 30-day closing range, the more the coin keeps rising over the next 10 days.
- `023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d2_wide-range-distance-continuation` (from F4, F5, F2): The farther a coin's daily close sits from the middle of its 30-day closing range, the more the coin keeps moving in that direction over the next 10 days, up from above the middle and down from below it, the more so the wider that 30-day range is against its middle.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
