---
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound_1d
idea tested: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4491 USD
---
## Findings
- **F1:** The next-day rebound after a low close grows with volume, not only above the tested 2x cut. The slope of the next-day excess return on close location (0 at the high, 1 at the low) is 0.04 % at t 0.20 for volume under 0.7x its 20-day mean (n 5644). It is 0.97 % at t 1.82 for 1.5–2x (n 1223), 1.74 % at t 2.78 for 2–3x (n 846) and 4.38 % at t 3.18 above 3x (n 446). A close in the bottom fifth of the range on volume above 3x is followed by +3.64 % (n 63).
- **F2:** On heavy-volume days the close-location effect sits in the coin's most volatile third. Split by 20-day volatility tercile, the slope is 6.49 % at t 4.77 in the high tercile (n 433), against 1.05 % at t 1.11 in the middle (n 427) and -0.50 % at t -0.72 in the low (n 432).
- **F3:** A large down day on heavy volume reverses more the next day than a large down day on normal volume. Down moves are measured against 20-day volatility. In a regression of next-day excess return on the down move, log volume ratio and their product, the product's coefficient is -0.0022 at t -3.61 (n 14500). In the lowest down-move quintile, heavy days are followed by +0.98 % against +0.32 % on normal-volume days. All days in that quintile give +0.42 % at t 4.37 (n 3007).
- **F4:** A wide day predicts a next-day rise beyond what the day's own return explains. The day's high-low range is measured against its prior 20-day average. With the day's volatility-scaled return in the regression, its coefficient is +0.0025 per unit at t 4.75 (n 15076). The widest range quintile is followed by +0.26 % at t 2.17, while the other four quintiles sit between -0.03 % and -0.10 %.
- **F5:** The heavy-volume low-close effect is a one-day effect. On a non-overlapping 3-day grid its slope falls to 2.67 % at t 1.54 (n 447), and 2.71 % at t 1.21 once the day's return is controlled. For down moves in general, the 2-day reversal holds at t -2.85 (n 7498) and the 3-day at t -1.94 (n 4859).
- **F6:** The tested effect is uneven over time and coins, which fits the book's failed Calmar.

## Ideas
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.g1_volume-graded-low-close-rebound` (from F1, F5): On a day when a coin's volume is above its 20-day average, the closer its close sits to the day's low, the more the coin rises over the next 1 day. The heavier that day's volume relative to its 20-day average, the stronger this rebound.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.g2_volatile-regime-absorption-rebound` (from F2, F6): When a coin's 20-day volatility is high, a heavy-volume day closing near its low is followed by a larger rise over the next 1 day. The nearer the close sits to the low, the larger that rise.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.g3_heavy-volume-capitulation-reversal` (from F3, F5): The larger a coin's 1-day fall relative to its 20-day volatility, and the heavier that day's volume relative to its 20-day average, the more the coin rises over the next 1 day.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.g4_range-expansion-next-day-rise` (from F4): The wider a coin's daily high-low range relative to its 20-day average range, the more the coin rises over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
