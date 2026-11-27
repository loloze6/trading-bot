---
line: 7.d confirmed, not profitable
backtest: 074-01.b1.d3.d2_agitated-deep-run-fade_1d
idea tested: 074-01.b1.d3.d2_agitated-deep-run-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4261 USD
---
## Findings
- **F1:** The book fails only on its falls against its gain (Calmar 0.60 against 0.75). The cause is that it trades almost nothing: it holds a position on 4 % of the coins' days, at a mean size of 0.36 of the book, and earns +4.1 % a year. On folds B and C its deepest fall (-1.68 %) is one long stretch of 477 days over w9 to w13 with 18 losing days. In w7, w10 and w12 the book earns exactly 0, so a few losing cases are never paid back by enough winning ones.
- **F2:** The falling-agitated profile throws away most of the effect. Run-breaking up days that the profile did not trade (regime "chop", 845 cases) still fall the next day by +0.79 % against the coin's drift, in the short direction (t 4.40). In falling markets alone, the breaks outside the profile earn +1.81 % (t 4.79, 203 cases), against +2.65 % for the held ones (t 3.95, 83 cases).
- **F3:** The effect lives in a falling market, calm or agitated, as the brief says. Breaks after a 30-day fall earn +1.82 % in calm markets (t 3.76, 157 cases) and +2.34 % in agitated ones (t 5.32, 129 cases). Breaks after a 60-day fall below -10 % earn +1.34 % (t 4.60, 253 cases). In rising markets the breaks earn nothing: -0.17 % (t -0.55, 232 cases) on the 30-day trend and -0.39 % (t -1.04, 176 cases) on the 60-day trend.
- **F4:** The falling market is not an effect of its own. Over the same next day, non-break days in a 30-day fall earn +0.03 % (t 0.23, 1900 days) and non-break days in a 60-day fall earn -0.01 % (t -0.10, 1649 days). Run-breaking up days in the same markets earn +2.05 % (t 6.20, 286 cases). The condition belongs to the idea's own theory: trapped holders exist only in a downtrend.
- **F5:** Inside falling markets the fall still grows faster than the run's depth. By thirds of depth (the run's loss over the mean absolute daily move of 30 days), the next-day unusual move is +1.09 % for shallow runs (t 1.91, 96 cases), +1.59 % for middle ones (t 3.01, 94 cases) and +3.47 % for deep ones (t 5.81, 96 cases). In the held book the same thirds give +1.28 %, +1.41 % and +3.13 %. The convex sizing is right; the gate is too narrow.
- **F6:** Holding longer does not help. Held cases over 3 days give +1.60 % in total (t 2.04, 135 cases), barely above the one-day move of +2.04 % (t 4.32). The information is spent in the next day.
- **F7:** The held cases that lose are mostly outside a 30-day fall. Held breaks in a 30-day fall earn +2.68 % (t 3.43, 71 cases), against +0.91 % in flat markets (t 1.23, 30 cases) and +0.94 % in rising markets (t 1.26, 20 cases). Held bars in a 30-day rise lose -0.23 % a day of book value (16 bars).
- **F8:** The per-case move is large against costs, so costs are not the problem. The total move is +1.05 % per case against a trade cost of 0.19 % (5.5 times). Opening the falling market roughly triples the cases (286 breaks in a 30-day fall against 83 held) at a similar or larger move per case. That adds gain on many more independent days, which lifts the yearly return faster than the depth of a fall made of single losing days.

## Ideas
- `074-01.b1.d3.d2.d1_falling-market-deep-run-fade` (from F1, F2, F3, F4, F5, F6, F7, F8): In a falling market, calm or agitated alike, the first up day after a run of consecutive down days is followed by a fall in the coin's close over the next day, and that fall grows faster than the run's depth (the run's loss over its down days against the coin's usual daily move over the last 30 days), concentrated after the deepest runs.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
