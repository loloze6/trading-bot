---
line: 7.g patterns
backtest: 035-01_wide-low-close-rebounds_1d
idea tested: 035-01_wide-low-close-rebounds
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4306 USD
---
## Findings
- **F1:** The rebound sits only in the widest days that close near their low. Days in the coin's widest third of range against its prior 14-day average range, closing in the bottom fifth of the day's range, rose +1.40 % more than the coin's normal drift the next day (t 3.01, 451 cases on 195 days). Narrow days near their low rose +0.13 % (t 0.30, 315 cases) and mid-width days near their low +0.06 % (t 0.14, 385 cases). The tested product spreads this effect thinly over every bar, which is why its measured size is only +0.11 % per case against a 0.19 % trade cost.
- **F2:** The test's forecast does not grade evenly. The bottom three per-coin forecast quintiles all fell short of the drift the next day (−0.31 %, −0.25 % and −0.43 %, t −1.58, −1.44 and −2.01). Only the top quintile was clearly positive, at +0.69 % (t 2.62, 1741 cases on 550 days), so the slope's t of 3.27 comes from the extreme end.
- **F3:** The rise from wide days near their low does not reverse. On a non-overlapping 3-day grid these days ended +2.07 % above the coin's 3-day drift (t 2.42, 154 cases on 69 days). On the same grid, narrow days near their low ended −1.58 % (t −1.10, 109 cases). The day after next added nothing either way for wide days near their low: −0.19 %, t −0.46, 451 cases.
- **F4:** A large one-day fall on a wide day rebounds, graded by the width. Days in the coin's lowest fifth of one-day return rose +1.02 % above drift the next day when the day was in the widest third (t 2.71, 928 cases on 300 days). They rose +0.45 % at mid width (t 1.09, 456 cases) and fell −0.07 % at narrow width (t −0.08, 151 cases). Across all widths the lowest fifth of one-day returns rose +0.69 % (t 2.36, 1725 cases).
- **F5:** The book behaves like a long position in the coins, not like the idea. It held a position on 100 % of coin-days. On its best 5 % of days it gained +5.2 % while the coins gained +8.6 %. On its worst 5 % it lost −5.1 % while the coins lost −9.5 %. Its gains and its falls track the market's own large days, which is consistent with a Calmar of 0.56.
- **F6:** No other angle stood out given how many I looked at:

## Ideas
- `035-01.g1_wide-low-close-three-day-rebound` (from F1, F3, F2): The wider a day's high-to-low range is against the coin's average daily range over the past 14 days, and the nearer its close sits to the day's low, the larger the coin's rise over the next three days.
- `035-01.g3_extreme-wide-low-close-rebound` (from F2, F1, F5): The wider a day's high-to-low range is against the coin's average daily range over the past 14 days, and the nearer its close sits to the day's low, the larger the coin's rise over the next day, growing faster than in proportion as the day becomes extreme.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `035-01.g2_wide-sharp-fall-next-day-rebound` (from F4, F1): The larger a coin's one-day fall, and the wider that day's high-to-low range against its average daily range over the past 14 days, the larger the coin's rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
