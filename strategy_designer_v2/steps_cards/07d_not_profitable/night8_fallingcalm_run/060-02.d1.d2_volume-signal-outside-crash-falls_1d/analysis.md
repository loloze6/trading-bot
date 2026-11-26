---
line: 7.d confirmed, not profitable
backtest: 060-02.d1.d2_volume-signal-outside-crash-falls_1d
idea tested: 060-02.d1.d2_volume-signal-outside-crash-falls
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6202 USD
---
## Findings
- **F1:** The check failed on Calmar (0.32 against 0.75, yearly +7.1 %). The book's deepest fall in folds B and C is -11.0 % and lasts 356 days, from w9 to w12. In those fall windows (w10–w12) the shorts were taken at a 20-day return of only -1.8 % on average, against -10.2 % for the shorts in the other windows. They lost 0.48 % a day, against a gain of 0.19 % a day elsewhere.
- **F2:** The volume signal works only once the 20-day fall is more than slight. In falling-profile grid cases (non-overlapping), growing volume minus shrinking volume over the next 5 days is +7.1 % (Welch t 3.76, 113 cases; volume-ratio vs 5-day-return correlation 0.32) when the 20-day return is from -20 % to -5 %. It is -1.4 % (t -0.88, 142 cases) when the 20-day return is from -5 % to 0.
- **F3:** On the signal's own grid cases, the move in the signal's direction over 5 days grows with the depth of the 20-day fall: +4.4 % at -20 % to -10 % (119 cases), +2.5 % at -10 % to -5 % (47 cases), +0.6 % at -5 % to 0 (70 cases).
- **F4:** The depth condition alone, without the signal's side, is one-sided. On falling grid bars the coin's 5-day excess is -3.0 % (t -2.65, 84 cases) at a 20-day return of -20 % to -10 %, and -3.4 % (t -1.87, 29 cases) at -10 % to -5 %. Split by volume inside a deeper moderate fall, the coin falls when volume shrank and does not when it grew: shrinking tercile -6.6 % (t -3.58, 39 cases), growing tercile +0.8 % (t 0.55, 35 cases).
- **F5:** Keeping the book's held positions only on bars with a 20-day return below -5 % improves the approximate book before costs:
- **F6:** Positions carried into crash days (20-day return below -15 %) still earned: +0.36 % a day for shorts (342 days) and +0.15 % for longs (185 days). Restricting the book to -20 % to -5 % lowers its Calmar to 1.32, against 1.95 for all 20-day returns below -5 %. In the falling grid, the crash-depth spread of growing minus shrinking volume is +3.2 % (t 1.52, 146 cases).
- **F7:** The signal's move keeps growing past 5 days. On 235 non-overlapping signal cases, the move in the signal's direction is +2.5 % at 5 days (t 2.99), +3.2 % at 10 days (t 3.09) and +4.8 % at 20 days (t 3.25), against a trade cost of 0.19 %.

## Ideas
- `060-02.d1.d2.d1_volume-signal-in-deeper-falls` (from F1, F2, F3, F4, F5, F6): In a falling market, the more the coin's trading volume over the past 30 days has grown against the 30 days before, the smaller its fall, or the larger its rise, over the next 5 days, and the more so the deeper its 20-day fall has gone, except when its 20-day return is only a slight dip, where volume tells nothing.
- `060-02.d1.d2.d2_volume-dry-up-longer-hold` (from F2, F3, F7): In a falling market, while the coin's 20-day return is clearly negative, the more its trading volume over the past 30 days has grown against the 30 days before, the smaller its fall, or the larger its rise, over the next 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
