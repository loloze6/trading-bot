---
line: 7.g patterns
backtest: 060-02.d2_volume-growth-recent-ten-day-fall_1d
idea tested: 060-02.d2_volume-growth-recent-ten-day-fall
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4137 USD
---
## Findings
- **F1:** The tested idea's effect sits mostly in its strongest dry-up cases. On the active 5-day grid (folds B, C; 437 cases), the most negative forecast quintile (mean forecast -18.5, 88 cases) is followed by an unusual move of -4.74 % (t -4.17, cases not grouped by day). The next two quintiles give only -0.47 % (t -0.43) and -0.93 % (t -0.87).
- **F2:** The volume-growth side is not graded. The fourth quintile (forecast +4.8) gives +4.08 % (t 2.28), but the top quintile (forecast +17.0) gives only +1.36 % (t 0.88). The long trades average +2.95 % before fees, against +4.92 % for the shorts.
- **F3:** Recomputed from prices on all falling-market grid bars, the largest 30-day volume shrinkage gives the same result. Its bottom quintile (log ratio -0.76, 81 cases) is followed by -3.59 % against the coin's drift (t -2.76), while the top quintile (+0.85) gives +0.49 % (t 0.32).
- **F4:** The volume effect needs the 10-day fall to still be running. On falling-market bars with a 10-day return at or above 0, the slope of the next 5-day unusual move on the volume ratio is -0.015 (t -0.67, 139 cases, 43 days), so there is no continuation there.
- **F5:** In the book, the short side earned most of the gain and the long side carried the worse tails:
- **F6:** Outside the tested situation, nothing stood out across the angles I examined. These were choppy-market volume, choppy-market 5-day returns, volatility, range, close location and weekday. The only choppy-market signal was a volume-ratio slope of -0.031 (t -1.51, 445 cases), and its sign changed across the years (2018 +0.011, 2021 -0.102). The non-monotone quintile spikes (close location quintile t -3.34, range quintile t -2.44) do not stand out against the number of looks.

## Ideas
- `060-02.d2.g1_volume-dry-up-deepens-fall` (from F1, F2, F3, F4, F5): In a falling market, while the coin's 10-day return is still negative, the more its trading volume over the past 30 days has shrunk against the 30 days before, the larger its fall over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
