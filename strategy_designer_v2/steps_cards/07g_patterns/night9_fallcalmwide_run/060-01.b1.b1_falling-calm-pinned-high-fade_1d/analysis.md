---
line: 7.g patterns
backtest: 060-01.b1.b1_falling-calm-pinned-high-fade_1d
idea tested: 060-01.b1.b1_falling-calm-pinned-high-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4500 USD
---
## Findings
- **F1:** Across all wide days (width at or above its 75th percentile, 1.89, folds B and C), the lower the close in the range times the width, the higher the next day's unusual return; the link holds in every profile split: agitated Spearman 0.215 (n 892, p 8e-11), calm 0.147 (n 1174, p 4.5e-7), falling 0.206 (n 538, p 1.4e-6), rising 0.143 (n 608, p 4e-4), choppy 0.137 (n 209, p 0.048).
- **F2:** In a falling calm market, wide days closing in the top third of their range are followed by an unusual next-day return of -1.05 % (t -2.02, 84 cases on 45 days); wide falling-calm days closing in the middle or bottom third show none (-0.23 %, t -0.34; -0.16 %, t -0.20).
- **F3:** The book's own short cases in folds B and C gain 2.06 % per case in the short direction (t 2.80, 30 cases on 23 days), against 0.42 % (t 0.90, 122 cases) over all four folds, so folds A and D carry the weakness.
- **F4:** Pinning the close to the high adds nothing: over all profiles, the widest-quarter days closing in the top tenth have an unusual next-day return of -0.09 % (t -0.18, 239 cases), against -0.55 % (t -1.43, 479 cases) for closes at 0.7 to 0.9 of the range.
- **F5:** The falling-calm fade lasts one day only: wide calm days closing in the top third have a 3-day unusual return of +0.19 % (t 0.24, 163 grid cases on 76 days).
- **F6:** In a rising calm market, wide days closing in the bottom third rebound by +1.94 % unusual over the next day (t 3.05, 92 cases on 49 days); this is the only profile cell of the 18 read where that rebound has a t above 2.4.
- **F7:** The wide low-close rebound appears in every year read, 2018 +0.63 % (t 0.77), 2019 +0.46 %, 2020 +1.46 %, 2021 +1.85 % (t 2.48), 761 cases in all.
- **F8:** These do not stand out as patterns: weekday (every |t| < 1.2), the volume surge quintile (+0.52 %, t 1.93), and large down days scaled by the 30-day swing (rz below -1: +0.80 %, t 1.91 for -2 to -1). The last is already held many times in the map's agitated cells.

## Ideas
- `060-01.b1.b1.g1_falling-calm-graded-high-close-fade` (from F2, F1, F4, F5, F3): In a falling, calm market, the higher a day closes within its high-to-low range, scaled by how wide that range is against the coin's 30-day swing of daily returns, the larger the coin's fall over the next day.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `060-01.b1.b1.g2_rising-calm-wide-dip-rebound` (from F6, F1, F7): In a rising, calm market, the lower a day closes within its high-to-low range, scaled by how wide that range is against the coin's 30-day swing of daily returns, the larger the coin's rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
