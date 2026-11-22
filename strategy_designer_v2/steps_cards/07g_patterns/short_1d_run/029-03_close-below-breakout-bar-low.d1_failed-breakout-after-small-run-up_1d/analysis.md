---
line: 7.g patterns
backtest: 029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up_1d
idea tested: 029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3720 USD
---
## Findings
- **F1:** The book's shortfall comes from how rarely it is in a position, not from cost. It held a short on only 1.4 % of grid bars (48 of 3,419) and made 89 trades over six coins and 24 windows, which is 0.00485 trades per day. Its 308 days with a non-zero return averaged +0.31 % a day (t 1.65), against a per-case total move of 2.24 % on a trade that costs 0.19 %.
- **F2:** The plain failed breakout does not predict a fall. On 245 non-overlapping 5-day cases, a close back below the prior 20-day closing high within 3 days of closing above it was followed by an unusual move of +0.26 % (t 0.36). Only the deeper failure the test used, a close below the breakout day's low, carried the confirmed fall: +2.83 % short-side, t 2.73, 50 cases. On the book's active grid bars the 5-day unusual return was −1.23 % (t −1.07, 48 cases).
- **F3:** Fresh 20-day closing highs were followed by a 5-day unusual move of +1.62 % (t 2.18, 306 cases), which goes against the brief's short side. This does not stand out as a finding. The breakout's size does not grade it (Spearman 0.07, p 0.22). Most of it comes from XRP (+10.2 %, 36 cases) and from 2020 and 2021 (+5.3 % and +8.4 %), while 2022 was −3.6 % (t −2.4).
- **F4:** Failed breakdowns, a close back above the prior 20-day closing low within 3 days of closing below it, were followed by +1.63 % over 5 days (t 2.29, 209 cases). The recovery terciles rise from +1.08 % to +1.54 % to +2.27 %, but the Spearman between recovery size and the move is 0.03 (p 0.66), so the effect is not graded and does not stand out as a finding.
- **F5:** Calendar and recent-return groupings show scattered extremes that do not pass the bar set by the number of looks. Grid bars starting Monday were followed by +1.43 % (t 2.89, 498 cases) and Tuesday by +1.40 % (t 2.74, 475), and Monday was positive in both halves of the period (+1.71 % and +1.15 %). The second-lowest 1-day-return quintile was followed by −1.48 % (t −3.53), but it is not monotone with its neighbours (+0.33 % below it, −0.08 % above). Volatility level, relative volatility, position in range and bar range showed no |t| above 1.9.

## Ideas
- No ideas: I looked at about seventy groupings (forecast and position, trades, 20-day breakouts and failures both ways, 1-, 5- and 20-day returns, volatility level and rank, range position, bar range, weekday, year, the book's active days). No pattern beyond the tested idea is both graded and strong enough to stand apart from chance: the largest t values, near 2.2 to 3.5, are what that many looks produce, and the breakout and failed-breakdown effects are not graded (Spearman 0.07 and 0.03).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
