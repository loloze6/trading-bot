---
line: 7.g patterns
backtest: 061-01.g1.d1.d2.g2_choppy-swing-scaled-move-continues_1d
idea tested: 061-01.g1.d1.d2.g2_choppy-swing-scaled-move-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6492 USD
---
## Findings
- **F1:** Large 5-day moves continue over the next 5 days in calm markets, and this holds in every trend. On non-overlapping 5-day grids, the slope of the drift-adjusted next 5-day return on the 5-day move in 30-day swing units is 0.0144 in rising calm (t 2.21, 182 cases), 0.0106 in choppy calm (t 2.03, 176 cases) and 0.0129 in falling calm (t 1.85, 161 cases). Calm here means a 30-day swing at or below the coin's median.
- **F2:** The same slope in agitated markets is weak or flat. It is 0.0016 in rising agitated (t 0.31, 136 cases), -0.0017 in falling agitated (t -0.31, 240 cases) and 0.0104 in choppy agitated (t 0.62, 73 cases). The tested idea's "choppy" profile mixes calm and agitated, which helps explain its slope t of only 1.11 and its strength of 0.006.
- **F3:** The effect shows only at the 5-day horizon, not at shorter ones. The calm slopes over the next 1 and 3 days are small and unsure: rising calm t 0.75 and 0.63, choppy calm t 1.17 and 0.88, falling calm t 1.63 and 1.30.
- **F4:** The brief's own single-day move also points the same way at 5 days in calm markets. The slope of the next 5-day return on the one-day move in swing units is 0.026 in rising calm (t 2.11), 0.018 in choppy calm (t 1.98) and 0.014 in falling calm (t 1.13). It is negative in choppy agitated (-0.017, t -1.12).
- **F5:** The tested book lost on its shorts. Its 559 short trades averaged -1.21 % net (median -1.86 %), against +1.25 % for its 428 longs. Trades on XMR averaged -1.52 % over 188 trades. The book earned +2.8 % a year, and its Sharpe was 0.31 below holding's.
- **F6:** Two other patterns were found but are already held in the map. In falling agitated markets, larger down days rebound the next day (slope -0.021, t -2.60, 636 days). Outside the choppy profile, days closing in the lowest fifth of their range are followed by +0.58 % drift-adjusted the next day (t 2.14, 1463 cases). Up days in falling agitated markets lean towards a fall, -1.09 % in the top tercile, but with t -1.57, which does not stand out after this many angles.

## Ideas
- `061-01.g1.d1.d2.g2.g1_calm-swing-scaled-move-continues` (from F1, F2, F3): In a calm market, the larger a coin's 5-day move against the standard deviation of its daily returns over the past 30 days, the further it keeps moving the same way over the next 5 days, after a rise as after a fall.
- `061-01.g1.d1.d2.g2.g2_calm-big-day-five-day-follow-through` (from F4, F3, F2): In a calm market, the larger a coin's one-day move against the standard deviation of its daily returns over the past 30 days, the further it keeps moving the same way over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
