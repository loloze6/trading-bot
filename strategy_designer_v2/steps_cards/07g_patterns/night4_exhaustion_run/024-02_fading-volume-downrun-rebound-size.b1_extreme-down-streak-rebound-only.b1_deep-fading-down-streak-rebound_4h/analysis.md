---
line: 7.g patterns
backtest: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only.b1_deep-fading-down-streak-rebound_4h
idea tested: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only.b1_deep-fading-down-streak-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4612 USD
---
## Findings
- **F1:** Volume over the last day (6 bars), measured against the coin's 30-day mean volume, predicts the next 3 days in the direction opposite to the brief: on the non-overlapping 3-day grid, the top fifth by each coin's own ranking is followed by +1.06 % excess return (0.118 of a usual 3-day move, t 3.36, 1062 cases) and the bottom fifth by −0.78 % (t −3.09, 1062 cases); the rank correlation is +0.063 overall and positive in all six coins (0.042 to 0.097) and all eight years (0.003 to 0.108).
- **F2:** The volume effect is strongest after a falling day: when the last day's return was negative, the top quarter of volume is followed by +1.16 % excess over 3 days (t 3.09, 645 cases) and the bottom quarter by −0.60 % (t −1.82); after a rising day the top quarter gives only +0.49 % (t 1.25); the rank correlation is 0.079 after falls and 0.051 after rises.
- **F3:** The bar range over the last day, against its 30-day mean, behaves like volume and is slightly stronger: rank correlation +0.073 with the next 3 days' excess return, positive in all six coins (0.045 to 0.093); the top fifth is followed by +0.78 % (t 2.19) and the bottom fifth by −0.67 % (t −2.70); it keeps t 2.13 in a joint regression in which volume drops to t 1.19.
- **F4:** The last day's return, in usual moves, reverses over the next 3 days: rank correlation −0.053 (p 0.0001, 5292 cases); the bottom fifth (the sharpest one-day falls) is followed by +0.79 % excess (t 2.76, 1059 cases); in the joint regression it keeps t −3.37, while the 3-day past return carries the opposite sign (t +3.54).
- **F5:** The tested idea moves almost nothing: +0.05 % unusual move per case over 3 days (strength 0.007, t 0.37, 4039 cases), against a cost of 0.19 % per trade; the book's 1 % worst days (−13.2 %) and best days (+14.8 %) match the coin's own moves on those days (−13.0 % and +14.7 %), so its tails are the coin's tails held long, which is why Calmar fails (0.39).
- **F6:** Grid points on a Sunday are followed by −0.15 of a usual 3-day move (t −4.05, 811 cases), lower in all six coins (−0.11 to −0.22) and in 6 of 8 years; their last-day volume is much lower (log ratio −0.57 against −0.11 on other days), so this effect is mostly the low-volume pattern of F1 seen through the calendar.

## Ideas
- `024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only.b1_deep-fading-down-streak-rebound.g1_heavy-volume-precedes-rise` (from F1, F6): The more a coin's volume over its past day exceeds its 30-day average, the more the coin rises over the next three days; the more that volume falls short of the average, the more the coin lags its normal drift.
- `024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only.b1_deep-fading-down-streak-rebound.g2_high-volume-fall-rebounds` (from F2, F4): After a coin falls over its past day, the higher that day's volume relative to the coin's 30-day average, the larger the coin's rise over the next three days.
- `024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only.b1_deep-fading-down-streak-rebound.g3_range-expansion-precedes-rise` (from F3): The wider a coin's bar ranges over its past day relative to their 30-day average, the more the coin rises over the next three days.
- `024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only.b1_deep-fading-down-streak-rebound.g4_one-day-fall-reverses` (from F4, F5): The larger a coin's fall over its past day, counted in its usual one-day move over the last 30 days, the larger its rise over the next three days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
