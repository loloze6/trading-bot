---
line: 7.g patterns
backtest: 058-02.b1.b1_quiet-volume-fall-keeps-falling_1d
idea tested: 058-02.b1.b1_quiet-volume-fall-keeps-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4235 USD
---
## Findings
- **F1:** Inside the tested 30-day-fall regime, the middle of the depth range keeps falling, but the deepest falls do not. The drift-adjusted 5-day return by 30-day-return quintile runs from deepest to shallowest as +1.19 % (t 0.46, 51 days), -2.27 % (t -1.96), -3.90 % (t -4.04, 74 days), -2.29 % (t -1.78) and -0.40 % (t -0.39). The middle quintiles 1 to 3 are negative in 9 of the 12 windows.
- **F2:** The volume the idea grades on changes nothing. Its forecast buckets give -1.29 %, -1.31 %, -0.04 %, -2.48 % and -0.82 % with no order and every |t| under 1.4. Within middle-depth falls, the light, middle and heavy short-volume terciles all keep falling (-4.85 % t -2.91, -2.82 % t -2.06, -4.80 % t -2.61). This goes against the brief's claim that heavy-volume falls carry on less.
- **F3:** In calm stretches the continuation is roughly graded with depth. By depth quintile, calm bars give -3.06 % (n 25), -0.82 %, -3.86 % (t -2.91), -2.91 % (t -1.71) and +0.53 % (t 0.49) for the shallowest. Agitated bars instead reverse in the deepest quintile (+2.13 %, t 0.75, 113 cases).
- **F4:** In a choppy market (60-day return between -10 % and +10 %), the 30-day return scaled by its swing predicts the next 5 days in the same direction.
- **F5:** The same scaled-momentum slope is absent in the other trends: falling agitated t -0.27, rising agitated t 0.01, rising calm t 1.51, falling calm t 1.70.
- **F6:** The remaining angles showed nothing beyond chance:

## Ideas
- `058-02.b1.b1.g1_calm-scaled-fall-continues` (from F1, F2, F3): In a calm market, the larger a coin's fall over the past 30 days measured in its own usual daily swings, the more it keeps falling relative to its normal drift over the next 5 days.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `058-02.b1.b1.g2_choppy-market-scaled-momentum` (from F4, F5): In a choppy market, the larger a coin's 30-day return measured in its own usual daily swings, the more it moves the same way over the next 5 days, up after a rise and down after a fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
