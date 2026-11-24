---
line: 7.g patterns
backtest: 031-03.b1_up-streak-continuation-more-coins_1d
idea tested: 031-03.b1_up-streak-continuation-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4139 USD
---
## Findings
- **F1:** The book is mostly a scaled-down long position in its coins, not a timing effect. It held a position on 97 % of coin-days. Its daily returns correlate 0.92 with holding the coins, with a beta of 0.59. It earned 0.087 % a day against 0.128 % a day for holding, with a daily standard deviation of 2.70 % against 4.22 % (2898 days).
- **F2:** The 5-day unusual move does not grow with up-streak length on the non-overlapping grid. Streaks of 0 to 6+ days give means between −0.91 % and +1.10 %, all with |t| < 1 (66 to 3296 cases each). The order is not monotone: +1.10 % at 3 days, −0.91 % at 4, +0.15 % at 6+.
- **F3:** Down streaks show no graded giveback or continuation either. The move after a 3-day down streak is +1.49 % (t 1.84, 385 cases). After a 4-day down streak it is −2.94 % (t −1.98, 139 cases), and after 5 days −2.11 % (t −0.81, 64 cases). The sign alternates instead of growing with length.
- **F4:** A wider daily range against the coin's own last 20 days is followed by a higher 5-day unusual move, but the effect is not reliable. The pooled slope is 0.18 of a usual move per unit of percentile, t 1.81 (5121 cases, 518 days). The top two deciles give +1.47 % (t 1.73) and +1.46 % (t 1.51), against −0.75 % (t −1.15) in the bottom 20 %.
- **F5:** The range effect is not concentrated in a few coins: the range-percentile slope is positive for 15 of 18 coins. Only ADA (t 2.17) and AVAX (t 2.11) pass t 2, and BTC (t 0.05), LTC (t −1.08) and TRX (t −0.56) show nothing or the opposite.
- **F6:** The other angles show no pattern that survives the number of looks:

## Ideas
- No ideas: Across about fifteen angles (streak length on both sides, past returns, volatility, daily range absolute and relative, move size by sign, weekday, year, the book's extreme days), the strongest pattern is that a wide range relative to the coin's last 20 days precedes a higher 5-day move, but its pooled t is only 1.81. After that many looks it cannot be told apart from chance, so no finding supports a new idea.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
