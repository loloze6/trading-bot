---
line: 7.d not profitable
backtest: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week_4h
idea tested: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3894 USD
---
## Findings
- **F1:** Calmar fails because of one long fall: the book's deepest fall is 48 % (yearly return 34 %, Calmar 0.70). It runs 555 days, from w5 to w10, while the coins' average fell 59 %, and windows w5, w7, w9 and w12 lost 7 to 25 % with in-window falls of 21 to 33 %.
- **F2:** The book's gain comes from bars where the coin's 30-day return is positive. In position there, the mean gain is 6.7 bps per 4h bar outside w5–w10 (t 4.95, 18931 bars) and 5.4 bps inside them (t 2.24, 6397 bars). Where the 30-day return is negative, it earns 1.2 bps outside the fall (t 0.94, 13375 bars) and loses 2.9 bps inside it (t -1.29, 3973 bars).
- **F3:** The book spends 31 % of its in-position bars with a negative 30-day return. Gross of costs, staying flat there would have raised Calmar from 1.15 to 1.66, cut the deepest fall from 39 % to 29 %, raised the yearly return from 44 % to 48 % and raised the Sharpe from 1.06 to 1.30. Using the 60-day return instead gives a Calmar of only 1.27.
- **F4:** The same split shows on the 14-day return. In-position gain is -3.1 bps per bar in its lowest quintile (median -14 %, t -2.09, 9999 bars) and -1.1 bps in the next (t -0.82). It is 7.0, 7.2 and 5.8 bps in the upper three quintiles (t 4.5, 4.2, 2.6).
- **F5:** The quiet-week weighting points the wrong way. In-position gain is largest when the past 7 days were busier than the past 60: 11.7 bps per bar in the top quintile of the 7-day/60-day volatility ratio (median 1.48, t 3.48), against 1.1 to 2.2 bps in the three quietest quintiles (t 0.55 to 1.36).
- **F6:** The quiet-week weight ratio tells the same story. Gain is 8.9 bps per bar (t 2.72) in its top quintile (7-day range 1.53 times the 60-day range), against 1.9 to 3.5 bps below it.
- **F7:** The idea's own move is smaller than a trade's cost. Per case, the unusual move is +0.18 % over 3 days (strength 0.020, t 1.13, 3102 cases), 0.9 times the 0.19 % round-trip cost. The total move is +0.58 %, 3.0 times the cost, so the book earns mostly from the coin's drift, which it takes while the coin is rising.
- **F8:** Trades win only 44 % of the time (median net -0.22 %, mean +1.49 %, held 78 hours on average). Their worst 5 % lose about 9 %, whatever the entry's volatility ratio or 30-day return.

## Ideas
- `019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.d1_breakout-inside-rising-month` (from F1, F2, F3, F4, F7): When a four-hour bar closes above the highest high of a coin's preceding two-day narrow stretch, the coin rises over the next three days, larger the narrower that stretch was compared with the coin's 30-day average four-hour range, only while the coin's own 30-day return is positive.
- `019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.d2_breakout-after-busy-week` (from F5, F6, F7): When a four-hour bar closes above the highest high of a coin's preceding two-day stretch, the coin rises over the next three days, and the rise is larger the more active the coin's past 7 days were compared with its past 60 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
