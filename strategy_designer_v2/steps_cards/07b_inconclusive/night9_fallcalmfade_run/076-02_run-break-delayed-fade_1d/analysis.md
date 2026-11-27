---
line: 7.b inconclusive
backtest: 076-02_run-break-delayed-fade_1d
idea tested: 076-02_run-break-delayed-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3517 USD
---
## Findings
- **F1:** The fall shows mostly on the first day after the break and is almost absent on days 2 and 3, the only stretch the test read. On folds B and C, over 2,042 cases, the excess short return is +0.54 % on day 1 (t 2.59) but only +0.08 % on days 2 and 3 (t 0.27). Step 5's own measure on all folds was +0.06 % (t 0.33).
- **F2:** Measured from the up day's close over days 1 to 3, the fade is clear. Weighted by abs(forecast) as the plan weights it, it is +1.07 % (t 2.79, 2,086 cases on 647 days). Weighted by run length it is +1.04 % (t 2.71).
- **F3:** Over days 1 to 3 the fade grows with the run's length, as the brief says. The slope is +0.67 % per down day (t 3.75), against +0.29 % (t 1.93) on days 2 and 3 alone.
- **F4:** The fade is nothing after a single down day and grows with longer runs:
- **F5:** How large the up day was matters little, as the brief predicts. By quartile of the up day's size, the excess short return over days 1 to 3 is +0.38 %, +0.92 %, +0.99 % and +0.11 %, with no rise from small to large up days.
- **F6:** The effect is not uniform over time, which adds to the noise.
- **F7:** It is spread across coins. The forecast-weighted fade over days 1 to 3 is positive on all six, with t from 1.20 (LTC) to 2.76 (XMR).

## Ideas
- `076-02.b1_run-break-three-day-fade` (from F1, F2, F3, F4, F5, F7): In any market, after the first up day that ends a run of down days, the price falls over the next three days counted from that up day's close, and this fall is larger the more down days the run held.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
