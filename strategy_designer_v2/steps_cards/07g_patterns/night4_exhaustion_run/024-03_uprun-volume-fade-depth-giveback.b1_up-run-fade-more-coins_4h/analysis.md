---
line: 7.g patterns
backtest: 024-03_uprun-volume-fade-depth-giveback.b1_up-run-fade-more-coins_4h
idea tested: 024-03_uprun-volume-fade-depth-giveback.b1_up-run-fade-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4553 USD
---
## Findings
- **F1:** Over the next 3 days (18 bars, non-overlapping grid, coin drift removed), the coin's return rises steadily with its past-1-day volume against its 30-day mean volume. The bottom quintile (0.34× usual volume) gives −0.83 % (t −3.91, 2128 cases) and the top quintile (2.25×) gives +0.85 % (t +3.73, 2127 cases). In a joint regression with the past 1-day move and the down-streak loss, log relative volume keeps its slope (coefficient +0.0080, t +5.54). The top quintile beats the bottom on every coin (share 1.0) and in 6 of 8 years.
- **F2:** The gradient in F1 shows on both sides of the past day's move. After a 1-day fall, the volume quintiles run from −0.53 % to +1.39 % (top t +4.39, 995 cases). After a 1-day rise, they run from −0.88 % (t −3.77) to +0.60 % (t +1.86).
- **F3:** The largest down-streak losses are followed by a 3-day rise. The largest quintile of down streaks (mean −4.85 usual 4h moves) gives +1.28 % drift-adjusted (t +4.04, 1050 cases), against −0.50 % to −0.87 % in the three smallest quintiles. The joint regression keeps the slope (−0.0029 per usual move of loss, t −4.33), and the mean is positive on every coin (share 1.0). It is uneven by year: +4.98 % in 2020 (t 5.52), +4.15 % in 2024 (t 4.69), and negative in 2018 and 2021.
- **F4:** The past 1-day move on its own adds nothing once volume and the down-streak loss are in the regression. Alone, its lowest quintile gives +0.94 % (t +4.88), but its joint coefficient is −0.0001 (t −0.41).
- **F5:** The tested short side points the wrong way, and the book is effectively a short on the coin.
- **F6:** The 4h bar opening at 16:00 UTC has a drift-adjusted next-bar return of +0.073 % (t +6.67, 37206 bars), positive in 6 of 8 years. It is a fixed time-of-day condition, not a graded situation.

## Ideas
- `024-03_uprun-volume-fade-depth-giveback.b1_up-run-fade-more-coins.g1_heavy-volume-precedes-rises` (from F1, F2, F4): The heavier a coin's traded volume over the past day relative to its average daily volume over the past 30 days, the higher the coin's return over the next 3 days. The lighter the volume, the more it lags its normal drift.
- `024-03_uprun-volume-fade-depth-giveback.b1_up-run-fade-more-coins.g2_deep-down-streak-rebound` (from F3, F4): After an unbroken streak of falling four-hour periods, the coin rises over the next 3 days, and the rise grows with the streak's loss measured in the coin's typical four-hour moves over the past 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
