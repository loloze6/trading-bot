---
line: 7.g patterns
backtest: 003-04_heavy-volume-drop-continues_1d
idea tested: 003-04_heavy-volume-drop-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3299 USD
---
## Findings
- **F1:** After a down day of at least one usual move, the next day's return above the coin's average rises steadily with the day's volume against its 30-day mean: +0.0010 (t 0.53, n 568) for a ratio up to 1, +0.0024 (t 1.17, n 509) for 1–1.5, +0.0062 (t 2.01, n 276) for 1.5–2, +0.0120 (t 2.56, n 206) for 2–3, and +0.0197 (t 2.29, n 107) above 3; the Spearman correlation is 0.081 (p 0.00095, n 1666).
- **F2:** The rebound after heavy-volume falls (ratio ≥ 1.5, z ≤ -1) is not carried by one coin or one period: it is positive in all six coins (+0.0057 to +0.0145, four with t > 2), in 7 of 8 years (2024 is -0.0010), and in both halves of the windows (+0.0070, t 2.05, n 292; +0.0143, t 3.46, n 297).
- **F3:** The heavy-volume rebound builds over several days: excess return of +0.0121 over 2 days (t 2.67, 314 non-overlapping cases) and +0.0305 over 3 days (t 3.70, 178 cases); by 5 days it has faded, with sharp heavy falls (z ≤ -2) at -0.0033 (t -0.22, n 43).
- **F4:** Up days show no such grading: after a rise of at least one usual move, the next-day excess return goes from -0.0018 (t -1.01) at a volume ratio up to 1 to -0.0038 (t -0.66) above 3, with no step of |t| above 1.3. The volume effect belongs to falls only.
- **F5:** The tested short book is on the wrong side of this pattern: on its 634 active days it lost 0.00443 a day on average, and its Sharpe is -0.50.

## Ideas
- `003-04_heavy-volume-drop-continues.g1_heavy-volume-falls-rebound` (from F1, F2, F3, F4, F5): When a coin falls over one day on volume above its own 30-day average daily volume, it rises more than usual over the next 3 days, and the heavier that day's volume against the average, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
