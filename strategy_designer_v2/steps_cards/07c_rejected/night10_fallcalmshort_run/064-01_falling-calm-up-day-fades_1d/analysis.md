---
line: 7.c no effect
backtest: 064-01_falling-calm-up-day-fades_1d
idea tested: 064-01_falling-calm-up-day-fades
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3721 USD
---
## Findings
- **F1:** The test found no fade after scaled up days in falling calm markets. Over 3 days the unusual move was -0.23 % in the short direction, with t -0.69 over 746 cases on 443 days. The larger-forecast half did 0.26 % worse than the smaller half.
- **F2:** The market did the opposite of the idea after the larger rises. In falling calm bars, on the 3-day grid, days whose rise was 0.5 to 1 of the 30-day swing were followed by an unusual rise of +2.16 % (14 cases). Days of 1 to 1.5 swings were followed by +1.53 % (7 cases). The slope of the 3-day unusual move on the scaled rise was positive, +0.0071 per swing unit (t 0.80, 80 up-day cases), and more so over 5 days (+0.034, t 1.48, 39 cases).
- **F3:** The grading runs against the idea, and most clearly over 5 days. Over all up days in falling calm (raw rise in swing units, 104 cases on 88 days), the larger-rise half fell 2.87 % less than the smaller half (Welch t -2.11). The slope of the short-direction unusual move on the scaled rise was -0.025 per unit (t -2.04). Over 7 days the slope was -0.028 (t -1.52, 81 cases).
- **F4:** Up days as a whole were followed by underperformance only at longer horizons, and it is not certain. Taking every falling calm up day (first per grid cell), the short-direction unusual move was +0.42 % over 3 days (t 0.81, 119 days), +0.83 % over 5 days (t 1.09) and +2.20 % over 7 days (t 1.85, 68 days, strength 0.165). It was +2.07 % over 10 days (t 1.47) and +3.89 % over 14 days (t 1.80, 44 days).
- **F5:** That longer underperformance is mostly the coin's usual drift failing to appear, not a fall. The total short-direction move was +0.01 % over 7 days and -0.55 % over 5 days, against a trade cost of 0.29 %, so a short book on these days earns nothing before costs.
- **F6:** Where the 7-to-10-day shortfall holds:
- **F7:** Multi-day rises do not show the graded fade either. Over 3 days, the slope of the short-direction move on the 2-day scaled rise was -0.013 (t -1.10, 79 cases), and on the 3-day scaled rise it was -0.004 (t -0.29, 61 cases).

## Ideas
- `064-01.c1_feeble-bounces-fail-in-calm-declines` (from F3, F4, F2, F5): In a falling, calm market, the smaller a coin's one-day rise measured in units of its own 30-day standard deviation of daily returns, the larger the fall in its close over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
