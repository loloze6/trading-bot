---
line: 7.b inconclusive
backtest: 003-01_thin-volume-rise-reverses_1d
idea tested: 003-01_thin-volume-rise-reverses
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3359 USD
---
## Findings
- **F1:** The test's 5-day result is close to zero rather than just short of the bar: the main measure is -0.00142 with t -0.30 over 999 active grid cases. Note that -forecast/10 × excess is positive when the coin rises, so this small negative mean actually leans slightly toward giveback. The supporting check agrees (-0.0022), but the result is about 7 times too weak to reach |t| = 2.
- **F2:** The size of the forecast does not order the outcome. Across the active 5-day cases, mean excess by forecast quintile runs from most negative forecast to least: -0.0022 (t -0.33), +0.0041, -0.0020, -0.0137 (t -2.02), +0.0047. Across all thin-volume up days, rank correlation of rise × thinness with the following excess return is -0.019 (p 0.61, n 735) at 5 days and -0.014 (p 0.36, n 4151) at 1 day.
- **F3:** The effect is not in any coin but swings with the period. By coin the 5-day measure's t ranges only from -0.56 to +0.63. By year it moves from +2.44 in 2021 to -2.72 in 2022 and -3.12 in 2024. The market's own moves set its sign.
- **F4:** At 1 day the active bars do give back: mean next-day excess -0.0020, t -3.29, n 5482. This is a general fade of ordinary up days, not a thin-volume or large-rise effect. Small thin up days show -0.0018 (t -2.80, n 3975) and small heavy up days -0.0017 (t -1.39). Large thin up days, the idea's core case, show +0.0005 (t 0.12, n 176).
- **F5:** The clear volume-dependent effect in this data is on the other side, and opposite to the brief. After falls on above-average volume, the larger the fall times log volume ratio, the higher the next return. Rank correlation is 0.098 (p 0.000002, n 2376) over 1 day and 0.138 (p 0.0002, n 741) over 3 days. Large heavy-volume down days are followed by +0.0065 next-day excess (t 2.71, n 638), while large thin-volume down days show -0.0004 (t -0.12, n 168).
- **F6:** Heavy-volume rises show a positive 5-day mean, but it is not graded. The strength-weighted measure has t 2.02 (n 505), yet the rank correlation is 0.027 (p 0.55). The weakest quintile (+0.024, t 2.54) does as well as the strongest (+0.029, t 2.14).

## Ideas
- `003-01_thin-volume-rise-reverses.b1_heavy-volume-falls-rebound` (from F5, F4): When a coin falls sharply over one day on volume above its own 30-day average daily volume, it rebounds over the next 3 days. The larger the fall in units of its 20-day volatility and the heavier the volume against that average, the larger the rebound.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
