---
line: 7.g patterns
backtest: 031-01.b1.e2_wide-day-in-strong-run_1d
idea tested: 031-01.b1.e2_wide-day-in-strong-run
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3539 USD
---
## Findings
- **F1:** The one pattern that stands out is in the volatility-scaled 5-day return (the 5-day return over the 20-day standard deviation of daily returns), and it is a step, not a slope: on the non-overlapping 3-day grid, its top fifth is followed by a 3-day excess return of +0.96 % (t 3.26, 943 cases), while the other four fifths all sit between -0.14 % and -0.21 % (|t| < 1). That t is not clustered by day, and the six coins move together on the same days, so the evidence is weaker than it looks.
- **F2:** The day's range adds nothing graded inside up-runs: across range-ratio fifths 0 to 4 the 3-day excess is +0.30 %, +0.26 %, +0.09 %, -0.57 % (t -1.68) and +1.20 % (t 2.78, 515 cases). Only the widest fifth stands out, and that is the same top-tail step as F1.
- **F3:** The brief's flat close does not set the wide up-run days apart. Wide days in up-runs with a small body (under a quarter of the range) are followed by +1.82 % (t 2.04, 77 cases), wide days with a big body by +1.70 % (t 2.64, 266 cases), and middle bodies by only +0.17 % (t 0.23, 172 cases). Where the close lands in the range does not separate them either: +1.25 %, +1.16 % and +1.21 % for low, middle and high closes.
- **F4:** After down-runs, wide days show no move back of the run and no continuation: +0.42 % (t 1.02, 428 cases). Flat-close wide days in down-runs give -0.85 % (t -0.89, 69 cases).
- **F5:** Weekday is the largest effect seen, but it cannot become an idea: the 3-day excess after a Monday bar is -1.20 % (t -3.97, 680 cases) and after a Saturday bar +1.18 % (t 3.86, 676 cases). These t are unclustered on coins that move together, and a weekday is an on/off condition, not a graded situation. My day-clustered check of it (round 2) failed to run.
- **F6:** Neither the size of the day's own move nor the volatility level grades what follows. Across the 1-day z-move sevenths only one cell departs from zero (the sixth, -0.76 %, t -2.80), with its neighbours at -0.11 % and +0.39 %, so it is not monotonic. The volatility terciles give -0.10 %, -0.06 % and +0.31 % (t 1.24 at most).

## Ideas
- No ideas: About 40 cells were examined (range fifths by run direction, body and close location on wide days, size of the day's move, volatility-scaled run strength, volatility level, weekday, forecast fifths, coin). None of them shows a graded pattern outside the tested idea that survives this many looks and the correlation between coins. The strongest, the run-strength top-fifth step (F1), is a step rather than a slope and is already contained in the tested idea's rise-strength component. The weekday effect (F5) is unclustered and an on/off condition, not a graded situation.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
