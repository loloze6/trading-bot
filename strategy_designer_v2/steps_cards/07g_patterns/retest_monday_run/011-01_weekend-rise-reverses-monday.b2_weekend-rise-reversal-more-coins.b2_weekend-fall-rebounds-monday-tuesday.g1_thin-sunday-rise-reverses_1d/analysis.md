---
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_thin-sunday-rise-reverses_1d
idea tested: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_thin-sunday-rise-reverses
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4864 USD
---
## Findings
- **F1:** Shorting a Sunday rise pays in the book's daily returns, but the size of the rise and the thinness of Sunday's volume do not grade it. By size quintile of the Sunday rise, the unusual 2-day move in the short's direction runs +1.60 %, +1.28 %, +0.54 %, +1.20 %, +0.94 % (about 433 cases each). By volume-ratio quintile, from thickest to thinnest, it runs +1.42 %, +1.10 %, +0.69 %, +1.13 %, +1.21 %. Step 5's supporting difference was only 0.007 %.
- **F2:** After every Sunday close the coin underperforms, so much of the Sunday reversal is a calendar effect rather than a graded one. Across all Sundays, the coin's 2-day return minus its drift is −0.26 % (t −2.15, 4272 cases). Thursday is +0.33 % (t 3.19) and Friday +0.28 % (t 3.10). Measured as a move against the Sunday's sign, Sunday rises reverse by +1.11 % (t 6.54, 2167) and Sunday falls rebound by +0.63 % (t 3.88, 2105).
- **F3:** A Sunday fall rebounds more over the next 2 days the larger the fall. By fall-size quintile, smallest to largest, the rebound is −0.30 %, +0.45 %, +0.52 %, +1.54 % (t 4.58), +0.96 % (t 2.22), about 419 cases each.
- **F4:** Monday's move reverses over the next 2 days in a mostly graded way. By Monday-move quintile, from largest fall to largest rise, the 2-day return minus drift is +1.25 % (t 4.83), +0.04 %, −0.43 %, −0.73 % (t −3.17), +0.35 %, about 853 cases each.
- **F5:** A large rise late in the week continues over the next 2 days. Friday's top rise quintile is followed by +0.93 % minus drift (t 3.86, 852 cases), against −0.19 % after its largest falls. Thursday's top rise quintile is followed by +1.02 % (t 3.64, 855 cases).
- **F6:** The Sunday-rise reversal is not concentrated on Monday. Monday's day gives back +0.36 % (t 3.05) and Tuesday's day +0.48 % (t 4.32), over 2167 cases.
- **F7:** A Sunday rise reverses more after a falling week. When the 7-day move is in its lowest quintile, the reversal is +1.77 % (t 5.28, 434 cases), against +1.03 % in the top quintile. The middle quintiles are not monotonic, with +0.35 % in quintile 3.

## Ideas
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_thin-sunday-rise-reverses.g1_monday-fall-rebounds-midweek` (from F4): A coin's Monday move reverses over the next 2 days: the larger Monday's fall, measured in the coin's usual one-day moves over the past 60 days, the more the coin rises from Monday's close to Wednesday's close.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_thin-sunday-rise-reverses.g2_sunday-fall-rebounds-graded` (from F2, F3): A coin whose Sunday close is below its Saturday close rises over the next 2 days, and the larger Sunday's fall in the coin's usual one-day moves over the past 60 days, the larger that rise.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_thin-sunday-rise-reverses.g3_friday-rise-carries-weekend` (from F5): A coin's Friday rise continues over the next 2 days: the larger Friday's rise, measured in the coin's usual one-day moves over the past 60 days, the more the coin rises from Friday's close to Sunday's close.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_thin-sunday-rise-reverses.g4_sunday-bounce-after-falling-week` (from F1, F7): A coin whose Sunday close is above its Saturday close falls over the next 2 days, and the more the coin fell over the 5 days before that Sunday rise, measured in its usual one-day moves over the past 60 days, the larger that fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
