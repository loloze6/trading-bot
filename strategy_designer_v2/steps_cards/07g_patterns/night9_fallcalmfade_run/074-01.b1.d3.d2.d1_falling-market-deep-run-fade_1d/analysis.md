---
line: 7.g patterns
backtest: 074-01.b1.d3.d2.d1_falling-market-deep-run-fade_1d
idea tested: 074-01.b1.d3.d2.d1_falling-market-deep-run-fade
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.5670 USD
---
## Findings
- **F1:** In falling markets (60-day return below −10 %), the first up day after a down run is followed by a next-day short gain of +1.14 % above drift (t 2.86, 556 cases, 191 days); in rising markets the same up day gives −0.36 % (t −0.98, 447 cases) and in choppy markets +0.60 % (t 1.39, 183 cases), so the tested effect belongs to falling markets.
- **F2:** Among falling-market run breaks, the short gain rises with run depth in usual moves (Spearman 0.136, p 0.0013, 556 cases): the top depth tercile gives +2.01 %, +2.30 % and +3.06 % (t 2.03, 3.34, 3.52), while the low and mid terciles are mostly not distinguishable from zero (−0.66 % to +1.50 %).
- **F3:** Inside the deepest-run tercile, the short gain grows with the size of the breaking up day (small up +2.01 %, mid +2.30 %, big up +3.06 %, t 3.52 on 69 cases). Run depth plus up-day size ranks the next day slightly better than depth alone (Spearman 0.150, p 0.0004, against 0.136), though up-day size alone does not (0.053, p 0.21).
- **F4:** Up days in a falling market that are not run breaks (continuation up days) are not followed by a fall: −0.39 %, −0.47 % and +0.32 % across up-size terciles (all |t| < 0.9, 417 cases). Break up days give +1.11 %, +0.82 % and +1.52 % (t 1.98, 1.62, 2.56).
- **F5:** Among all falling-market up days, those ending the deepest 5-day slide (bottom quartile of 5-day return in usual moves) give a next-day short gain of +1.92 % (t 2.79, 241 cases, 99 days) and +2.81 % over the next 3 days (t 2.66, 232 cases); the other three quartiles give −0.48 % to +0.47 % (all |t| < 0.9).
- **F6:** The effect is a one-day effect. Falling-market run breaks give +1.14 % at 1 day (t 2.86), +0.90 % at 2 days (t 1.49) and +1.43 % at 3 days (t 2.05), so almost all of it comes on the first day.
- **F7:** The breaks the book actually held earn +1.85 % (t 3.62, 283 cases) against +0.40 % (t 0.84, 273 cases) for the breaks it skipped. The book's position gains before costs (allocation × next return) are concentrated: windows w14 (1.33) and w7 (1.05) make up about 75 % of the 3.18 total, and 4 of 12 windows are negative.
- **F8:** Other angles do not stand out enough, given how many were looked at, and none fills an empty cell of the profile map:

## Ideas
- `074-01.b1.d3.d2.d1.g1_deep-run-large-relief-fade` (from F1, F2, F3, F4, F6): In a falling market, the first up day after a run of consecutive down days is followed by a fall in the coin's close over the next day, and the fall is larger the deeper the run's loss (in usual daily moves of the last 30 days) and the larger that up day itself (in the same usual moves), most of all when a deep run ends with a large up day.
- `074-01.b1.d3.d2.d1.g2_falling-slide-bounce-fade` (from F5, F4, F1): In a falling market, an up day that comes after a deep slide in the coin's 5-day return (measured in usual daily moves of the last 30 days) is followed by a fall in the coin's close over the next three days, and the deeper the 5-day slide, the larger that fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
