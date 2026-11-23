---
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility_1d
idea tested: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.5101 USD
---
## Findings
- **F1:** In calm markets, where the 20-day volatility is below the 60-day volatility, a coin's Wednesday move continues over Thursday and Friday rather than reversing: the mean continuation is +0.98 % in excess of drift (t 5.47, 1436 cases), and it is the strongest of the 14 weekday-by-regime cells.
- **F2:** That Wednesday continuation in calm markets shows on both days (Thursday +0.42 %, t 3.17; Friday +0.54 %, t 4.23), after both rises (+0.59 %, t 2.35) and falls (+1.36 %, t 5.30), and in 7 of 8 years (2018 +2.69 % t 3.68, 2022 +1.49 % t 4.08, 2025 +1.36 % t 3.29; only 2020 negative at −0.39 %).
- **F3:** The Wednesday continuation is not cleanly graded by move size: its quartiles of |z| give +0.58 % (t 1.79), +1.13 % (t 2.74), +0.33 % (t 0.98) and +1.90 % (t 5.34), so only the largest quarter stands clearly apart.
- **F4:** Across all Wednesdays, the continuation fades as volatility rises: the four lower quintiles of the 20/60 volatility ratio give +0.78 % to +1.16 % (t 2.26 to 3.78), and the top quintile gives −0.08 % (t −0.16).
- **F5:** The calm-market continuation also holds after Thursday's move: the contrarian measure there is −0.56 % (t −3.45, 1444 cases), and −1.58 % (t −4.04) for moves above one 60-day standard deviation.
- **F6:** The Sunday reversal grows with the volatility ratio itself, not only above the ratio of 1: by quintile of the ratio, Sunday's move is reversed by +0.72 % (t 2.48), +0.09 % (t 0.29), −0.11 % (t −0.29), +0.66 % (t 1.98) and +2.13 % (t 5.15, 528 cases); this rise is concentrated in the top two quintiles.
- **F7:** Monday's move also reverses over Tuesday and Wednesday while volatility is rising: the mean reversal is +0.87 % (t 3.63, 1146 cases), +1.08 % (t 2.80, 509 cases) for moves above one standard deviation, and it is positive in all 8 years but reaches t ≥ 2 only in 2023 (t 2.72) and 2025 (t 4.36).
- **F8:** The reversal sits in Sunday's own move, not the full weekend's: measured on the Friday-to-Sunday two-day move, the rising-volatility reversal is only +0.36 % (t 1.39), against +1.22 % (t 4.84) on Sunday's one-day move.
- **F9:** Against the brief, the rising-volatility Sunday reversal is not larger after low Sunday volume. By tercile of Sunday volume against its 20-day mean it is +0.70 % (t 1.48), +1.21 % (t 3.10) and +1.69 % (t 3.88), but by quintile it is flat and uneven: +1.62 %, +0.06 %, +1.33 %, +1.32 % and +1.80 %.
- **F10:** The book's trades split by side the opposite way to the bar measure. Longs after weekend falls average +2.23 % net (1488 trades, 63 % winners) and shorts after weekend rises −0.75 % net (1428 trades, 42 % winners), while the bars show the reversal larger after rises (+1.74 %, t 4.43) than after falls (+0.73 %, t 2.28).

## Ideas
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility.g1_calm-midweek-moves-continue` (from F1, F2, F3, F4, F5): In a calm market, where a coin's 20-day daily volatility is below its 60-day volatility, the coin's Wednesday move (its Tuesday-to-Wednesday close-to-close return) continues in the same direction over the next 2 days, and the larger the Wednesday move, the larger the continuation.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility.g2_sunday-reversal-grows-with-volatility` (from F6, F8): The higher a coin's 20-day daily volatility stands against its 60-day volatility, the larger the share of its Sunday move (its Saturday-to-Sunday close-to-close return) that reverses over the next 2 days.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility.g3_monday-move-reverses-midweek` (from F7): While a coin's 20-day daily volatility is at least its 60-day volatility, its Monday move (its Sunday-to-Monday close-to-close return) reverses over the next 2 days, and the larger the Monday move, the larger the move back.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
