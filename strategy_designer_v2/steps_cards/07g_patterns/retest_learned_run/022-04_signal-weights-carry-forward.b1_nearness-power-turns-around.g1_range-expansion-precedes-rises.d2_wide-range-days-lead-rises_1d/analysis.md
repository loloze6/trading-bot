---
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises_1d
idea tested: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3612 USD
---
## Findings
- **F1:** After a large down day the next day reverts upward: one-day returns sorted into septiles by the day's return over its prior 20-day volatility give a next-day excess return of +0.46 % (t 3.89, 2051 days) in the most negative septile, +0.15 % (t 1.39) in the next and −0.04 % in the third. The rise grades with the size of the drop. The most positive septile shows no mirror effect (−0.01 %, t −0.06).
- **F2:** The tested range signal is not graded. On the 5-day grid (3419 cases), quintiles of the range ratio give excess 5-day returns of −0.11 %, −1.32 % (t −3.55), −0.19 %, +0.68 % and +1.08 % (t 2.28). The pooled standardised slope t is 2.29, but per coin it runs from −1.14 (LTC) to +2.19 (XRP). This matches the inconclusive verdict (slope t 0.02 on forecast > 0).
- **F3:** Inside wide-range days the excess 5-day return does not depend on where the day closed or on the day's own return. By close-location tercile it is +0.96 %, +0.71 % and +1.02 % (slope t 0.40). By one-day-return tercile it is +0.88 %, +0.40 % and +1.42 % (slope t 0.66).
- **F4:** The 20-day momentum effect on the next 5 days changes sign from year to year, with slope t −3.21 in 2022, −3.17 in 2023, +2.14 in 2024 and +2.45 in 2025 (about 354 cases each). Nearness to the 30-day high also flips, from −2.88 in 2018 to +2.11 in 2020 to between −1.3 and −1.9 in 2022–2025. These weak effects' weights do not carry from one period to the next.
- **F5:** Saturday's daily excess return is +0.34 % (t 4.08, 2484 days) against −0.30 % on Thursday (t −2.70). The weekend-minus-weekday gap is clear only in XMR (+0.58 %, t 3.38); the other coins sit between −0.34 and 1.27 in t.
- **F6:** The book's trades show no gain that grows with the entry forecast. Mean net profit by entry-forecast quartile is +3.69 %, +3.98 %, +1.54 % and +5.04 % (about 1207 trades each). In rising years the book trails the coin, for example 2021 at +0.17 % a day against +0.41 % and 2025 at +0.07 % against +0.20 %.

## Ideas
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.g1_large-down-days-revert-next` (from F1): The larger a coin's one-day fall relative to its daily volatility over the past 20 days, the higher that coin's return over the next day above its usual daily drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
