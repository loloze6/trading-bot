---
line: 7.b inconclusive
backtest: 032-02.b1.e1.e1.e1_tight-range-breaks-rise-faster_1d
idea tested: 032-02.b1.e1.e1.e1_tight-range-breaks-rise-faster
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3572 USD
---
## Findings
- **F1:** On folds B and C, the raw tightness the idea names grades the 5-day rise after an upside break. Breakout bars whose 60-day closing range was narrower than the median (19.4 average absolute daily moves) were followed by an unusual 5-day move 8.4 % larger than the wider half (Welch t 3.43, 120 non-overlapping cases on 74 days). Spearman's rho between the ratio and the 5-day unusual move is -0.31, and it is -0.35 at 10 days and -0.38 at 20 days.
- **F2:** The test's forecast barely carries that tightness. It standardises the compression against its own past 61 values, so it correlates only -0.55 with the raw ratio. Its rank correlation with the 5-day unusual move is +0.09, and its quintiles show no order (+0.9 %, +8.4 %, -1.0 %, +7.9 %, +3.2 %, about 25 cases each). This is why step 5's upper-minus-lower difference came out at -1.15 % with Welch t -0.92: the test measured tightness against the coin's own recent tightness, not the tightness the idea states.
- **F3:** On the raw ratio the grading falls steadily. By quintile, from tightest to widest (mean ratio 10.7, 15.0, 19.3, 22.7, 31.8), the 5-day unusual move is +7.7 % (t 2.72), +4.5 % (t 2.72), +8.7 % (t 2.07), +0.3 % (t 0.12) and -2.9 % (t -1.46).
- **F4:** The tight-minus-wide gap points the same way on every coin and in every year shown.
- **F5:** Overall, upside breaks keep rising rather than failing. The 5-day unusual move across all breaks is +3.98 % (strength 0.30 of a usual move, t 2.59 with the cases of one day taken together, 74 days), and it grows to +10.6 % over 10 days and +14.3 % over 20 days. Step 5's full-data size was +1.76 % (t 2.55), which is 9.1 times the 0.19 % cost of a trade.

## Ideas
- `032-02.b1.e1.e1.e1.b1_raw-tight-range-breaks-rise` (from F1, F2, F3, F4, F5): When a coin closes above its highest close of the prior 60 days, the narrower its 60-day range of closes was against its average absolute daily move, read as that ratio itself rather than against the coin's own earlier ratios, the larger its rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
