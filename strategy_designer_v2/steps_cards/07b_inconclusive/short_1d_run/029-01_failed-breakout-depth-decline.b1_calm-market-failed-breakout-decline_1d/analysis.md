---
line: 7.b inconclusive
backtest: 029-01_failed-breakout-depth-decline.b1_calm-market-failed-breakout-decline_1d
idea tested: 029-01_failed-breakout-depth-decline.b1_calm-market-failed-breakout-decline
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5144 USD
---
## Findings
- **F1:** Step 5's main measure is zero, not short of the bar on the idea's side: over 615 cases the mean unusual 5-day move in the short direction is -0.11 % (t -0.27, strength -0.007). My own grid of 722 cases gives the same at every horizon: -0.20 % at 1 day (t -1.14), -0.09 % at 3, -0.14 % at 5 (t -0.35), -0.42 % at 10 (t -0.65) and -0.46 % at 20 (t -0.41). So more data of the same kind would not settle it.
- **F2:** The test could not check the idea's grading, because the forecast is pinned at its limit. 626 of 722 cases have a forecast of exactly -20. The median split therefore put all 615 cases in the bottom half and none in the top, and the supporting check returned None.
- **F3:** The raw component the forecast was built from (depth below the old high divided by 20-day volatility) is graded the way the idea says at 10 days, but no tercile is clearly positive. The 10-day unusual move is -3.25 % in the lowest tercile (t -2.33, 236 cases), +0.56 % in the middle (t 0.56) and +1.50 % in the highest (t 1.69, 230 cases). At 5 days the three terciles give only -0.97 %, +0.15 % and +0.41 %, all with |t| below 1.3.
- **F4:** Splitting each coin's failures by its own full-sample terciles of 20-day volatility gives the one clear split. Low terciles gain +1.31 % in the short direction over 5 days (t 2.43, 203 cases), high terciles lose -1.89 % (t -2.11), and low minus high has a Welch t of 3.07. At 10 days the low terciles gain +2.19 % (t 2.55). In the low tercile, 5 of 6 coins are positive, and BTC is the strongest at +2.67 % (t 2.91).
- **F5:** The F4 split does not survive a volatility measure known at the bar's close, so I cannot turn it into an idea. Ranking 20-day volatility against its own past 250 days gives -1.29 % in the low tercile (t -1.15, 84 cases). Ranking it within the window gives -0.26 % at 10 days (t -0.18). The ratio of 20-day to 120-day volatility gives -0.78 % in its low tercile (t -0.95). The Spearman correlation of de-meaned log volatility with the 5-day move is only -0.09.
- **F6:** The low-volatility cases of F4 are mostly the calm years: 80 of the 203 are in 2023 and 35 in 2024. The 5-day gain there is +1.01 % (t 1.82) in 2023 and +3.31 % (t 2.08) in 2024, against -0.22 % in 2020 and -0.05 % in 2022. The split looks like a few quiet years carrying it, not a graded effect within each coin's own history.
- **F7:** The market's rise drowns the short: the total 5-day move per case is -0.69 %, or -3.6 times the 0.19 % cost of a trade. Holding the coins went up after these failures, and the book's Sharpe is -0.46.

## Ideas
- No ideas: The main measure is zero (t -0.27 on 615 cases), and the only split that shows the effect (F4) depends on each coin's full-history volatility level and on 2023–2024. It disappears under every measure known at the bar's close (F5, F6), and the raw grading (F3) has no clearly positive part, so no amended or new idea rests on a clear finding.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
