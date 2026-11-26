---
line: 7.b inconclusive
backtest: 058-02.b1.b2.b1.b2.b2.e2_choppy-calm-edge-continuation_1d
idea tested: 058-02.b1.b2.b1.b2.b2.e2_choppy-calm-edge-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4335 USD
---
## Findings
- **F1:** Step 5's main measure is positive but near zero: a slope of 0.000394 with a day-clustered t of 0.87 on 1,050 grid cases over 322 days, using every fold and every coin available on daily bars, so the test cannot be rerun on more data at this bar size.
- **F2:** In folds B and C alone, the same 5-day slope is clearly positive (0.00207, clustered t 2.13, 236 cases on 114 days), so folds A and D, which hold the other 814 of the 1,050 cases, must carry a slope near zero or negative. The effect does not point the same way across folds.
- **F3:** In B and C the positive slope comes from one year. Without 2021 it falls to 0.00029 (clustered t 0.46, 173 cases), and without window w18 to 0.00074 (t 1.14). The directional excess move over 5 days is +5.95 % (t 3.73, 63 cases) in 2021, against +0.18 % (t 0.18) in 2019 and −0.53 % (t −0.62) in 2020.
- **F4:** The 10-day horizon shows the same pattern, not a better place for the effect. Its slope is 0.00364 (clustered t 2.00, 114 cases), but only 0.00036 (t 0.26) without 2021, and the 2021 directional excess of +11.5 % (t 4.16) carries it.
- **F5:** Neither side nor the strength of the case isolates the effect. The long-only slope has t 1.43 (120 cases) and the short-only slope t 0.55 (116 cases); at 10 days the short-side slope is negative (t −0.77). Cases near the edges (|range position| ≥ 10) give t 1.68, no stronger than cases near the middle (t 2.32), so the pull does not grow toward an edge as the idea says.
- **F6:** The effect differs from coin to coin. In B and C the directional 5-day excess runs from −2.11 % for ETH (t −1.11, 20 cases) to +10.0 % for LINK (t 3.93, only 8 cases); most coins sit at t under 1.6. No single coin or group carries a robust effect.

## Ideas
- No ideas: The continuation slope is positive only because of one year (2021, window w18) in the folds shown, and it vanishes on the full data (t 0.87). No side, edge strength, horizon or coin shows the effect clearly while it is absent elsewhere, so the theme's effect (choppy-calm range-edge continuation or reversion) is not in the data (F1–F6).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
