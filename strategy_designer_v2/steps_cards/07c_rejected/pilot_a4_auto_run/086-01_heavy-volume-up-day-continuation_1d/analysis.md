---
line: 7.c no effect
backtest: 086-01_heavy-volume-up-day-continuation_1d
idea tested: 086-01_heavy-volume-up-day-continuation
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3742 USD
---
## Findings
- **F1:** In falling calm markets, heavy-volume up days are followed by no more rise than light-volume ones, the opposite of the brief's claim. On the plan's 5-day grid, heavy-volume up days were +1.17 % unusual (t 0.73, 21 cases) against +2.91 % (t 1.63, 25 cases) for light-volume up days. Pooling all five grid offsets, heavy minus light is only +0.8 %, +0.7 % and +2.0 % in the small, mid and big day-move terciles, and no cell has a t above 0.7 (heavy: t 0.43, 0.67, 0.45).
- **F2:** Heavier volume does not bring a larger later rise. On up days, the Spearman correlation between the volume ratio and the unusual move is -0.129 at 3 days (p 0.27), -0.013 at 5 days (p 0.93) and +0.098 at 10 days (p 0.64). Across the five 5-day grid offsets it swings from -0.151 to +0.255.
- **F3:** The only positive result is one coin in one period. DOGE (windows w17 and w18 only, 2021) gives +9.4 % for heavy-volume up days (t 2.77, 13 cases) and +4.1 % for light ones (t 2.22, 23 cases). BTC and XMR, which hold most of the cases, give -0.93 % (t -0.92, 25 cases) and -0.45 % (t -0.33, 45 cases) for heavy-volume up days, and about the same for light ones. By year, up days are +4.3 % in 2021 (t 3.16, 70 cases), -2.4 % in <date>'s 2019 part (t -3.31, 66 cases) and -0.4 % in 2018 (t -0.34, 95 cases).
- **F4:** What the market did instead was carry on with its slow decline, on BTC and XMR, after up and down days alike, whatever the volume. Every BTC and XMR quintile of the day's move is followed by a negative 5-day unusual move: BTC -0.5 % to -2.5 %, and XMR -0.6 % to -2.3 % (t from -0.49 to -1.65). Down days on the plan's grid were -2.23 % (t -1.57, 55 cases), and heavy-volume down days -3.47 % (t -1.49, 22 cases).
- **F5:** The apparent grading by the size of the up day on the plan's grid does not hold up. There, the top two day-move quintiles were +3.07 % (t 2.55, 20 cases) and +3.26 % (t 1.43, 20 cases), and the Spearman of the day's return was +0.334. Pooled over all five offsets, the top quintile falls to +0.58 % (t 0.64, 99 cases), and the day-return Spearman ranges from -0.128 to +0.334 across offsets.
- **F6:** Other horizons show no hidden effect either. At 1 day, up-heavy days were -0.46 % (t -0.78, 86 cases); at 3 days, -0.21 % (t -0.13, 29 cases); at 10 days, +0.97 % (t 0.34, 14 cases). Each is no better than the matching light-volume up days (-0.23 %, +0.97 % and +1.70 %).

## Ideas
- No ideas: The theme's effect is not in the data. In falling calm markets, heavy-volume up days are followed by no more rise than light-volume ones at 1 to 10 days (F1, F6), and volume does not grade the later move (F2). The only positive result comes from DOGE in two 2021 windows, while BTC and XMR kept falling after up days of every kind (F3, F4, F5). That leaves no long-side variation on this theme a trader could act on.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
