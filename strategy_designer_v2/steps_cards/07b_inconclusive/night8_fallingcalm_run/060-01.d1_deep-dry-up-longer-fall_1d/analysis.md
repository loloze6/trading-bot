---
line: 7.b inconclusive
backtest: 060-01.d1_deep-dry-up-longer-fall_1d
idea tested: 060-01.d1_deep-dry-up-longer-fall
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3585 USD
---
## Findings
- **F1:** The test's own forecast loses the grading: on the 20-day grid in the falling profile, the short excess return regressed on |forecast| gives a slope t of 0.95 (92 cells), matching step 5's t of -0.015. On the same cells, the plain 30-day-over-30-day log volume ratio grades the fall with a slope t of 3.26 (164 cells), with t 2.65 at 5 days (677 cells) and t 2.82 at 10 days (328 cells).
- **F2:** The grading runs across the whole range of volume change, not only the deepest dry-ups. Over 20 days, falling-profile cells by quintile of the volume ratio give a mean short excess of +3.7 %, +7.8 % (t 2.41), +3.5 %, −3.0 % and −9.5 % (t −2.14), deepest shrinkage first (33 cells each). Shrunk-volume cells average +4.6 % (t 1.91, 92 cells), while grown-volume cells average −4.8 % (t −1.55, 72 cells).
- **F3:** Inside the shrunk cells alone, the 20-day slope on the volume ratio is weak (t 0.61, 92 cells) but holds at 5 and 10 days (t 2.08, 2.09). So the effect is the contrast between shrinking and growing volume, which the test's clip at 0 and standardisation against the last two months threw away.
- **F4:** The 20-day volume-ratio slope is positive on all six coins: t from 0.65 (BTC) to 2.38 (XRP), XMR 1.98. It is positive in every year but strongest in 2018: t 4.08 in 2018, then 0.07, 1.18 and 0.54 in the following years. At 5 days the slope is positive in every year too (t 2.22, 1.89, 0.59, 0.35).
- **F5:** The pattern is tied to the falling market. Outside it, shrunk-volume 20-day cells have a short excess of −7.7 % (t −1.75, 49 cells) against +1.0 % for grown volume (50 cells), the opposite of the falling-market result.
- **F6:** The effect fades by 40 days: the volume-ratio slope t is −0.11 over 82 cells, so the horizon should stay at 20 days or less. The 10-day quintiles show the same order as the 20-day ones: +3.3 %, +3.4 %, −0.9 %, −2.4 %, −2.2 % (about 65 cells each).

## Ideas
- `060-01.d1.b1_falling-volume-ratio-grades-fall` (from F1, F2, F4, F5): In a falling market, the more a coin's trading volume over the past 30 days has shrunk against the 30 days before, the larger its fall over the next 20 days, the fall growing steadily with the shrinkage, from coins whose volume grew to those whose volume dried up most.
- `060-01.d1.b2_dry-up-fall-over-ten-days` (from F1, F3, F6): In a falling market, the more a coin's trading volume over the past 30 days has shrunk against the 30 days before, the larger its fall over the next 10 days.
- `060-01.d1.b3_growing-volume-stalls-fall` (from F2, F5): In a falling market, the more a coin's trading volume over the past 30 days has grown against the 30 days before, the larger its rise over the next 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
