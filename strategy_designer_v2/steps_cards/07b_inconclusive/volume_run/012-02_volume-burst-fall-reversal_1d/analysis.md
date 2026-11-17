---
line: 7.b inconclusive
backtest: 012-02_volume-burst-fall-reversal_1d
idea tested: 012-02_volume-burst-fall-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3325 USD
---
## Findings
- **F1:** The volume-ratio effect shows at 1 day and fades after: on the same 440-odd thinned sharp-fall cases, the slope of excess return on volume ratio is +0.00715 with t 3.61 (n 443) over 1 day, then +0.00432 with t 1.59 (n 440) over 3 days, -0.0028 with t -0.79 (n 434) over 5 days, and -0.0025 with t -0.54 (n 421) over 10 days.
- **F2:** The highest-volume falls rebound on the next day and give it back afterward: the top volume-ratio tercile (mean ratio 3.58, n 148) has a mean excess return of +1.14% over 1 day, -0.25% over 3 days (which is why the supporting check failed) and -1.78% over 5 days, against -0.04%, -0.82% and -1.31% for the lowest tercile.
- **F3:** The 3-day slope changes sign from year to year, so the pooled t is diluted: it is strongly positive in 2020 (t 4.05, n 39) and 2024 (t 3.51, n 56), negative in 2021 (t -2.49, n 50) and 2022 (t -2.35, n 67), and small in the other four years.
- **F4:** No single coin carries the 3-day result: per-coin slopes range from -0.0014 (LTC, t -0.20) to +0.0078 (XMR, t 1.36), with 65 to 79 cases each and four of six coins positive, so the effect is small next to each coin's noise.
- **F5:** The slope is clearer in the strongest cases the brief describes, though these subsets are small: among the deepest third of falls it is +0.0081 (t 2.27, n 122), and among the third with the deepest lower wick it is +0.0115 (t 2.50, n 147).
- **F6:** The wick alone does not mark a rebound: the deepest-wick tercile has a mean 3-day excess return of -1.03% against +0.10% for the shallowest, and the 3-day slope on wick depth is -0.019 (t -0.77, n 440).

## Ideas
- `012-02_volume-burst-fall-reversal.b1_volume-flush-next-day-rebound` (from F1, F2): Among bars that fall sharply, the larger the bar's volume relative to the coin's 30-day average volume, the larger the price rise over the next 1 day.
- `012-02_volume-burst-fall-reversal.b2_volume-burst-fall-reversal-broadened` (from F3, F4): Among bars that fall sharply, the larger the bar's volume relative to the coin's 30-day average volume, the larger the price rise over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
