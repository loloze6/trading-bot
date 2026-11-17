---
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways_1d
idea tested: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4011 USD
---
## Findings
- **F1:** Over the next 2 days, Sunday's move is undone far more than any other weekday's move: against the Sunday bar's sign the mean excess return is +0.82% (t=5.08, n=2051), and +0.56% on Monday alone (t=4.71). The other six weekdays sit between −0.36% and +0.08% over 2 days, with t from −2.65 to 0.59. All 6 coins and all 8 years point the same way (coin t from 1.23 to 3.28; year means from +0.08% to +1.83%).
- **F2:** The book catches only part of the reversal in F1, and fees eat that part. It holds a position for Monday only, while about 30% of the 2-day reversal comes after Monday (0.56% against 0.82%). Its Monday mean is +0.080% (t=1.55, n=2484), but it pays a steady −0.041% on Sunday days (t=−19.2), which is the entry fee. On four of the other five weekdays it holds no position at all (mean exactly 0).
- **F3:** The Sunday reversal is not graded by size, which is why the supporting check failed. By Sunday z quintile, the 2-day excess return is +0.65%, +0.77%, −0.27%, −1.74% (t=−4.90) and −0.47% (t=−1.25). The largest weekend rises reverse less than the moderate ones, which is why the larger half of |forecast| had the lower reversal (−0.08% difference).
- **F4:** Contrary to the brief, low weekend volume does not deepen the reversal. The 2-day reversal after Sunday by relative-volume tercile is +0.65% when volume is low (t=2.43), +0.84% in the middle (t=3.16) and +0.97% when it is high (t=3.18), with 684, 683 and 684 cases.
- **F5:** On days other than Sunday, only the largest falls are followed by a next-day rebound. The bottom quintile of the daily return scaled by its 20-day standard deviation (mean z −1.40) is followed by +0.39% excess over the next day (t=3.86, n=2487); the other four quintiles lie between −0.11% and −0.07%, with no t beyond 1.1. All six coins are positive (XMR +0.75%, t=3.43), and 6 of 8 years are positive.
- **F6:** Saturday is the strongest calendar day. Holding the coin, Saturday's daily return is +0.45% (t=5.53, n=2484), and the bar after Friday's close earns +0.30% above the coin's mean (t=3.76, n=2479). That bar is positive in 6 of 8 years and for all 6 coins, but the book is flat on it.
- **F7:** Strong 5-day rises tend to continue, but the effect is not stable. The top quintile of the volatility-scaled 5-day return is followed by +0.63% excess over 2 days (t=3.34, n=1442). The fourth quintile is negative (−0.29%), and the top quintile is negative in 2019 and 2023, so the pattern is weak given how many angles I looked at.

## Ideas
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways.g1_large-daily-fall-rebounds` (from F5, F3): After a coin's own daily fall that is large against its 20-day volatility, the coin rises over the next 1 day, and the larger the fall in units of its usual daily move, the larger the rebound.
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways.g2_heavy-volume-weekend-move-reverses` (from F1, F2, F4): A coin's move over Sunday (UTC close-to-close) is retraced over the following 2 days (Monday and Tuesday), and the retracement is larger the higher the coin's Sunday volume relative to its 20-day average volume.
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways.g3_saturday-drift-after-strength` (from F6, F7): A coin rises over Saturday (UTC), and the rise is larger the larger the coin's rise over the preceding 5 days in units of its 20-day volatility.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
