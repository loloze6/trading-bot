---
line: 7.g patterns
backtest: 058-02.g1_choppy-agitated-dip-continues_1d
idea tested: 058-02.g1_choppy-agitated-dip-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3973 USD
---
## Findings
- **F1:** Over every bar of folds B and C, not only the profile, a deeper close below the 5-day closing high (in units of the 30-day daily swing) is followed by a lower drift-adjusted 5-day return: the slope is +0.0164 per swing unit, t 2.61 with cases of one day taken together, on 1,364 grid cases over 256 days. That is continuation, the opposite of the brief's recovery. The 5-day dip measured this way beats the 10-day distance (t 1.45), the raw unscaled 5-day dip (t 1.96) and the 5-day return z (t 1.62).
- **F2:** The continuation is graded at its two ends. The deepest quarter of non-zero dips (mean −2.63 swings) is followed by −2.97 % drift-adjusted over 5 days (t −2.15, 264 cases). Closes at their 5-day high are followed by +2.01 % (t 1.87, 308 cases). The two middle quarters are flat (+1.31 %, −0.87 %). The deep-dip move is about 15 times the 0.19 % cost of a trade.
- **F3:** The slope has the same sign across the sample. It is positive on all six coins (t 1.46 to 3.00), in all four years (2018 to 2021, t 0.80 to 1.57) and in 9 of 12 windows. It belongs to the 5-day horizon: at 2 days the slope is +0.0005 (t 0.20, 3,457 cases) and at 10 days +0.0183 (t 1.69, 674 cases).
- **F4:** In the brief's own profile, approximated (60-day return above +10 % and the 30-day swing at or below its in-window median), the dip slope is also continuation, not recovery: +0.047 with OLS t 4.23 on 179 cases, and the deepest third is at −2.08 %. For comparison, rising agitated gives +0.026 (t 1.51, 139 cases). This t does not group cases by day, and the window warm-ups make the profile approximate.
- **F5:** The tested book lost money for a mechanical reason: it was in the market on only 4.8 % of the bars, the choppy agitated profile. Its non-zero days correlate −0.75 with the coin's own daily return, and it was up on only 43 % of them (675 days).

## Ideas
- `058-02.g1.g1_rising-calm-dip-continues` (from F4, F1, F3): In a rising, calm market, the further a coin's close sits below its highest close of the past 5 days, measured against its usual daily swing over the past 30 days, the larger its fall over the next 5 days.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `058-02.g1.g2_scaled-5-day-dip-continues` (from F1, F2, F3): The further a coin's close sits below its highest close of the past 5 days, measured against its usual daily swing over the past 30 days, the larger its fall over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
