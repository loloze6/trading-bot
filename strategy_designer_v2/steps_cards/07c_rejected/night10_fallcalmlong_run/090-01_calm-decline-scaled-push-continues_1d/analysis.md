---
line: 7.c no effect
backtest: 090-01_calm-decline-scaled-push-continues_1d
idea tested: 090-01_calm-decline-scaled-push-continues
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3817 USD
---
## Findings
- **F1:** Inside the falling calm profile, the plan's measure has no slope on its own side, and the whole spread comes from the other side. On the explore windows' non-overlapping 5-day grid, coins with a positive 5-day scaled push rose only +0.96 % more than their drift over the next 5 days (48 cases). Within those positive pushes the slope was flat (t 0.04). Coins with a zero or negative push lagged by −3.26 % (73 cases; Welch t 2.34), and that lag kept growing: −4.04 % at 10 days and −5.90 % at 20 days.
- **F2:** The market rewards a longer push over a longer horizon than the plan tested, and only inside the profile. The 10-day scaled return predicts the next 10 days with slope 1.25 % per unit and t 2.73 (111 cases). The 3-day scaled return predicts the next 10 and 20 days with t 2.18 and 2.19. The plan's own 5-day push over 5 days gives t 1.53 (121 cases). Outside the profile, every one of these pairs has a t between −0.74 and 0.83 (492 to 593 cases), so the effect belongs to falling calm markets, as the brief says.
- **F3:** The quintiles show the steps sit at the bottom, not at the top. The two lowest 5-day-push quintiles lagged by −4.7 % and −4.1 % over 5 days, and by −5.4 % and −5.2 % over 10 days. The two highest gained +1.7 % and +0.3 % over 5 days. The top quintile gained +1.5 % over 10 days and +9.4 % over 20 days, but on only 25 cases.
- **F4:** The slope over 10 days is larger the deeper the coin's 60-day fall. In the deepest third (mean −43 %) and the middle third (−26 %), the slope was 2.12 % with t 1.89 and 1.89 % with t 2.04 (about 30 cases each). In the shallowest third (−16 %) it was 0.56 % with t 0.35.
- **F5:** The effect is uneven across years and coins. The 10-day slope was positive in 2018 (t 2.15) and 2021 (t 1.48) and negative in 2019 (t −1.42). By coin, ETH carries it (10-day t 2.12), while XMR and ZEC are weak (t 0.38 and 0.37). Every coin with enough cases shows the negative-push lag over 10 days, from −3.5 % to −7.3 %.

## Ideas
- `090-01.c1_calm-decline-ten-day-push` (from F2, F1, F3): In a falling, calm market, a coin's 10-day return divided by the standard deviation of its daily returns over the last 30 days predicts its rise over the next 10 days: the larger this scaled push upward, the larger the rise that follows, and the weaker or more negative it is, the smaller the rise.
- `090-01.c2_deep-calm-decline-push` (from F4, F2, F1): In a falling, calm market, a coin's 5-day return divided by the standard deviation of its daily returns over the last 30 days predicts its rise over the next 10 days, and the deeper the coin's 60-day fall, the larger the rise that follows a given scaled push.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
