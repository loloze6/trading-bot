---
line: 7.g patterns
backtest: 077-03.g1.b1_choppy-agitated-wide-high-close-fall_1d
idea tested: 077-03.g1.b1_choppy-agitated-wide-high-close-fall
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4354 USD
---
## Findings
- **F1:** Across all bars of folds B and C, a day closing in the bottom quarter of its range rebounds the next day, and the rebound grows with the day's width against the coin's 30-day swing: width quintiles 0 to 2 give -0.14 %, -0.13 % and +0.04 % (t -0.34 to 0.09), quintile 3 gives +0.87 % (t 1.87, 178 days) and quintile 4 gives +1.66 % (t 2.83, 334 cases, 138 days). High closes show no such grading: quintile 3 gives +0.17 % and quintile 4 gives -0.67 % (t -1.61) in the long sign.
- **F2:** Inside the choppy-agitated profile, wide days closing near their low rise the next day by +2.88 % beyond drift (t 2.52, 37 cases, 30 days), against +0.24 % for narrow ones and +0.49 % for mid ones. This is larger and surer than the tested side: wide high closes in the same profile fall by only -2.62 % (t -1.56, 30 cases).
- **F3:** Inside the profile, the next-day fall after a high close does not grow as the close nears the high. Closes at 0.75 to 0.9 of the range give -1.81 % (t -2.09, 91 cases, 72 days), but closes at 0.9 to 1.0 give +0.00 % (35 cases). The tested short gains from the day's width, not from how close the close sits to the high.
- **F4:** Outside the profile, wide low closes rebound in rising markets by +1.67 % (t 2.83, 148 cases, 65 days) and in falling markets by +1.28 % (t 1.61, 238 cases). In choppy markets they give only +0.10 % (t 0.12, 61 cases). In rising markets the rebound holds with both swing levels: +2.10 % (t 2.32, 24 days) with a high swing and +1.53 % (t 1.60, 29 days) with a low swing.
- **F5:** Wide high closes fall the next day in falling markets with a high swing, by -2.46 % (t -2.37, 61 cases, 29 days), against +0.05 % in falling markets with a low swing. They continue up in rising markets with a low swing, by +1.66 % (t 2.29, 139 cases, 73 days). Both patterns are already held: the first by 060-01.g1.d2.d1 (falling agitated, short), the second by 033-03.b2, 034-01.b1 and 035-01.b1 (rising calm). I leave them out.
- **F6:** The book acts rarely and its result sits in the tails. It has 126 mean-reversion bars out of 9,904 and 231 coin-days with a non-zero return. Its median active day returns -0.016 %, while the 5 % and 95 % quantiles are -1.35 % and +2.13 % and the 1 % and 99 % quantiles are -5.56 % and +6.22 %.
- **F7:** Neither weekday nor year carries a pattern in the next-day move. Weekday means give t between -1.09 and 1.44, and year means give t between -1.83 and 0.88.

## Ideas
- `077-03.g1.b1.g1_choppy-agitated-wide-low-rebound` (from F2, F1, F3): In a choppy, agitated market, a day that closes near its low is followed by a rise over the next day, and the rise is larger the wider the day's range against the coin's 30-day swing of daily returns.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `077-03.g1.b1.g2_rising-wide-low-close-rebound` (from F4, F1): In a rising market, a day that closes near its low is followed by a rise over the next day, and the rise is larger the wider the day's range against the coin's 30-day swing of daily returns.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
