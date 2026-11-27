---
line: 7.g patterns
backtest: 076-02_run-break-delayed-fade_1d
idea tested: 076-02_run-break-delayed-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4246 USD
---
## Findings
- **F1:** Over the 3 days after the close of an up day that ends a down run, the coin's move above its normal drift is graded by the number of down days the run held: +0.62 % after 1 down day (t 0.93, 385 cases, 147 days), -1.13 % after 2 (t -1.30, 208 cases), -2.66 % after 3 (t -2.97, 102 cases, 55 days), -2.26 % after 4 (t -1.43, 36 cases) and -3.58 % after 5 or more (t -1.88, 27 cases). Bars that break no run show +0.21 % (t 0.52, 2104 cases).
- **F2:** The slope of that 3-day excess move on the run's length is negative in each 40-day trend group: choppy -1.65 % per down day (t -2.83, 127 cases), rising -1.32 % (t -2.20, 198 cases), no 40-day history -1.11 % (t -2.08, 223 cases) and falling -0.44 % (t -1.08, 210 cases). The fade grows with the run whatever the market.
- **F3:** Breaks after a single down day are about half of all cases (385 of 758) and carry no fade (+0.62 %). The tested sizing still gave them about a quarter of the cap (forecast about 5), so they dilute the graded fall. This fits the verdict's weak weighted size: +0.34 % short, t 1.61.
- **F4:** The fade is not concentrated on days 2 and 3 after the break. The excess move from 1 to 3 days after the break has mixed signs at short runs: +1.19 % at 2 down days in a rising 40-day market and +1.67 % at 2 down days with no 40-day history. Only runs of 3 or more are negative on that span, for example -3.48 % (t -2.20) in choppy markets. The full 3 days from the break close is where the grading shows (F1).
- **F5:** When the coin fell over the 20 days before the break, the 3-day fade's slope on run length is negative in both halves of the windows shown: w7–w12 -1.18 % per down day (t -2.18, 160 cases) and w13–w18 -1.44 % (t -3.16, 177 cases). Runs of 3 down days fade -4.92 % (t -2.73) when agitated and -3.71 % (t -3.38) when calm. With runs of 2 or more, 9 of the 12 windows are negative.
- **F6:** In folds B and C, the book's daily returns correlate -0.83 with the coins' own daily returns, with a Sharpe of 0.40. The book was in a position on 84 % of coin-days. Most of what it earned or lost was a short bet on the coins' moves, not the run-break effect.

## Ideas
- `076-02.g1_run-break-fade-beyond-first` (from F1, F2, F3, F4): In any market, after an up day that ends a run of down days, the coin falls over the next three days from that up day's close, and the fall grows with the number of down days in the run beyond the first, with nothing after a run of a single down day.
- `076-02.g2_run-break-fade-after-decline` (from F5, F1): When a coin's 20-day return is negative, an up day that ends a run of down days is followed by a fall over the next three days, larger the more down days the run held.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
