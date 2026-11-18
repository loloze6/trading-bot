---
line: 7.d not profitable
backtest: 012-04_flush-depth-retracement-size_1d
idea tested: 012-04_flush-depth-retracement-size
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4919 USD
---
## Findings
- **F1:** The long lower wick that the tested situation requires marks the wrong falls. Sharp falls (one-day return at or below -2 of its 20-day standard deviation) with a wick of at least 0.3 of the range were followed by a next-day excess return of -1.46% (t -2.36, n=86) and a 3-day excess of -0.83%. The same falls without the wick were followed by +1.12% next day (t 3.33, n=324). The flush bars the book traded were followed by a next-day excess of -0.71% (t -1.17, n=89).
- **F2:** The book loses because of the bar after the flush. Its 88 trades were held about 1.03 days on average and returned -0.78% before fees and -0.88% after fees. That puts the mean daily return at -4.5e-05, Sharpe at -0.28 and Calmar at -0.09. The position size was not the problem: the mean allocation when held was 1.08.
- **F3:** The volume burst carries the rebound. Sharp falls with volume at least 2 times the prior 20-day median were followed by a 3-day excess of +1.02% (t 2.03, n=247) and a next-day excess of +0.95% (t 2.17). Sharp falls without the burst were followed by a 3-day excess of -1.04% (t -1.70, n=161).
- **F4:** The rebound is graded by depth among volume-burst sharp falls with no wick condition. Regressing the 3-day excess return on the open-to-low drop, scaled by its own 60-day mean, gives a slope t of 2.18 (220 independent cases). Return-depth terciles were followed by 3-day returns of +0.67%, +0.98% and +1.55%. The book's own wick-filtered flush bars showed no such grading (slope t -0.72, n=84).
- **F5:** The wick is graded against the rebound. Among volume-burst sharp falls, the next-day return by wick tercile was +1.67% (t 1.85), +0.51% and -0.37%. Among falls of at least 1.5 standard deviations, the next-day excess by wick tercile was +0.75%, +0.63% and -0.07%.
- **F6:** The wick condition also makes the book trade too rarely. The book trades 0.005 per bar. Volume-burst falls of at least 2 standard deviations without the wick rule give 0.0127 independent cases per bar. Volume-burst falls of at least 1.5 standard deviations give 0.0186 per bar, with a 3-day excess of +1.33% (t 2.77, n=320).

## Ideas
- `012-04_flush-depth-retracement-size.d1_deep-heavy-volume-fall-rebound` (from F1, F3, F4, F6): Among bars that fall sharply on a volume burst, the larger the bar's drop from its open to its low against its usual size over the last 60 days, the larger the price rise over the next 3 days. The rise is larger the nearer the bar closes to its low, rather than leaving a long lower wick.
- `012-04_flush-depth-retracement-size.d2_close-at-low-next-day-bounce` (from F1, F2, F5): After a daily fall on a volume burst at least 2 times the 20-day median, the shorter the bar's lower wick relative to its range, the larger the price rise over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
