---
line: 7.g patterns
backtest: 058-02.b1.g1_falling-market-rally-fades_1d
idea tested: 058-02.b1.g1_falling-market-rally-fades
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4112 USD
---
## Findings
- **F1:** In a falling market, where a close sits in its 20-day high-low range ranks the next days' unusual move in the same direction, not against it. On the 3-day grid the Spearman correlation is +0.116 (673 cases) and on the 5-day grid +0.176 (401 cases). Closes in the bottom fifth of the range are followed by a 3-day unusual move of -1.54 % (t -2.3, 224 cases) and closes in the middle fifth by +1.27 % (t 1.97, 117 cases). This is continuation from the low edge, the opposite of the brief's pull back to the middle.
- **F2:** The continuation from the bottom of the range in falling markets holds across years. Closes at or below a quarter of the 20-day range are followed by a 3-day unusual move of -2.23 % in 2018 (162 cases, 47 days, day-pooled t -1.34) and -2.39 % in 2019 (71 cases, 31 days, t -1.57). Only 2020 points the other way, on a small sample: +9.1 % on 15 cases.
- **F3:** In a choppy market the 5-day unusual move rises steadily with the close's position in its 20-day range, so the brief's reversion is not there.
- **F4:** In choppy calm markets alone the samples are too small to read the brief's own cell. There are 50 cases on the 3-day grid in total. The 0.2-0.4 band is followed by -3.75 % (t -2.40, 8 cases), again a fall from the lower part of the range rather than a rebound.
- **F5:** In a falling market the tested rally fade shows only in its top bucket, which cannot be told from chance after clustering.
- **F6:** Two more patterns did not hold up or are already held.

## Ideas
- `058-02.b1.g1.g1_choppy-range-position-continuation` (from F3, F4): In a choppy market, the nearer a coin's close sits to the bottom of its 20-day high-low range, the larger its fall over the next 5 days; the nearer to the top, the larger its rise.
- `058-02.b1.g1.g2_falling-market-range-low-continuation` (from F1, F2): In a falling market, the nearer a coin's close sits to the bottom of its 20-day high-low range, the larger its further fall over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
