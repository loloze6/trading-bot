---
line: 7.b inconclusive
backtest: 003-01_thin-volume-rise-reverses_1d
idea tested: 003-01_thin-volume-rise-reverses
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3452 USD
---
## Findings
- **F1:** The tested measure is flat rather than slightly short of the bar. Step 5 gives a mean 5-day excess return of -0.0018 with t = -0.50 on 930 events, and my recomputation stays near zero at every horizon (1 day: -0.0005, t -0.39, n 1186; 5 days: -0.0012, t -0.32, n 849; 10 days: -0.0076, t -1.09, n 611), so a different horizon would not have shown it.
- **F2:** The effect is mixed across periods and roughly cancels out: thin-volume rises were followed by giveback in 2018 (-0.026, t -1.59), 2019 (-0.017, t -2.05) and 2022 (-0.021, t -2.74), but by further rises in 2020 (+0.022, t +2.44) and 2021 (+0.037, t +2.57).
- **F3:** The split follows the coin's own 30-day trend: when the 30-day return was zero or negative, thin-volume rises gave back -0.0093 over 5 days (t -1.96, n 500). When it was positive, they rose a further +0.0104 (t +1.72, n 349), and +0.0217 (t +2.39, n 179) in the 0.5–0.75 volume band.
- **F4:** The grading the idea predicts is reversed, which is why the supporting check fails (+0.0018): the smallest standardised rises gave back -0.0107 (t -1.31, n 176), while the larger three quartiles rose further (+0.0065, +0.0062, +0.0091). Only the very-thin band leans the predicted way (≤0.5: -0.0074, t -1.42, n 439; 0.5–0.75: +0.0050, t +0.91, n 394).
- **F5:** The other half of the brief shows clearly and graded: daily rises above one usual move kept rising over 5 days as volume rose against its 30-day average. Rises on volume above 1.5× the average, split into thirds by volume, gave +0.0036 (t 0.45), +0.0179 (t 2.01) and +0.0258 (t 2.32), 181 events each, and +0.0221 (t 3.08, n 298) when the 30-day return was positive. Across all 1364 rises the correlation of the 5-day excess return with log volume ratio is +0.064.

## Ideas
- `003-01_thin-volume-rise-reverses.b1_thin-rise-reverses-in-downtrend` (from F2, F3, F4): When a coin rises sharply over one day on volume well below its own 30-day average daily volume, it gives back part of that rise over the next 5 days, only while its 30-day return is negative; the thinner its volume against that average, the larger the giveback.
- `003-01_thin-volume-rise-reverses.b2_heavy-volume-rise-continues` (from F5): When a coin rises sharply over one day on volume above its own 30-day average daily volume, it keeps rising over the next 5 days; the heavier that day's volume against its 30-day average, the larger the further rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
