---
line: 7.d not profitable
backtest: 024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise_4h
idea tested: 024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3674 USD
---
## Findings
- **F1:** The book fails on its falls: chained in window order, its daily returns fall 61.2 % at the deepest point against a yearly return of 34.4 % (Calmar 0.56). The deepest in-window falls come in w16 (-55.3 %, worst day -38.1 %), w2 (-51.0 %) and w14 (-50.5 %), windows where holding the coins lost 44 % in w2, lost 49 % in w14 and gained 36 % in w16.
- **F2:** The book falls with the market because it is a long-only book that stays mostly invested. On its worst 5 % of days (145 days) it lost 7.1 % on average while holding the coins lost 8.6 %. Its mean position is 0.62 to 0.80 of the book in every 30-day trend quintile.
- **F3:** The position's bar gains follow the coin's trailing 30-day trend, standardised by its usual move. In the most negative trend quintile the mean gain is -0.015 % per bar, summing to -2.30, with the worst bar at -41 %. In the most positive quintile it is +0.045 % per bar, summing to +7.16, with the worst bar at -18 %.
- **F4:** The surge cases are graded by the same 30-day trend. The excess 3-day return is -0.03 % (t -0.08, 658 cases) in the most negative trend quintile, rising to +0.47 % (t 1.50) and then +0.82 % (t 2.02, 658 cases) in the most positive. In the losing windows w2, w14 and w16, cases in a downtrend (trend z -1.22) lost 1.95 % excess (t -1.91, 131 cases), with a 10th-percentile 3-day return of -15.5 %.
- **F5:** The rise after a surge grows with the size of the surge bar's own move against the coin's usual 4h move, whichever its direction. By quintile of the absolute body z, the excess runs from -0.35 % (t -1.37) through -0.24 %, +0.44 % and +0.50 % to +1.23 % (t 3.75), with 802 to 803 cases each. Large down bodies (z -2.7) give +0.81 % (t 2.59) and large up bodies (z +2.6) give +0.86 % (t 2.64).
- **F6:** The forecast's own grading carries no information. By forecast level (3.4, 9.3, 19.7) the excess is +0.35 %, +0.23 % and +0.25 %, and the step-5 Spearman is -0.014. Overall, the unusual move of +0.21 % per case is only 1.1 times the 0.19 % cost of a trade.

## Ideas
- `024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise.d1_volume-surge-in-uptrend` (from F1, F2, F3, F4): When a coin trades a four-hour volume far above its 30-day average, it rises over the next three days, only while its 30-day return is positive. The higher the volume against that average and the stronger the coin's 30-day rise against its usual move, the larger the rise.
- `024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise.d2_large-bar-volume-surge-rise` (from F5, F6): When a coin trades a four-hour volume far above its 30-day average on a bar whose own move is large against the coin's usual four-hour move, it rises over the next three days. The larger that bar's move in either direction, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
