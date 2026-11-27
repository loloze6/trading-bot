---
line: 7.g patterns
backtest: 072-03_choppy-deep-down-day-continuation_1d
idea tested: 072-03_choppy-deep-down-day-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4150 USD
---
## Findings
- **F1:** The tested depth does not predict the next day in choppy markets. Across all 1,250 choppy bars the Spearman rho of depth against next-day excess return is 0.024 (p 0.39). On choppy down days the depth quintiles show no gradient: the deepest is −0.83 % (t −1.13, 125 cases) and the shallowest is +0.42 % (t 1.28). This matches step 5's size of −0.10 % per case (t −0.73, 926 days).
- **F2:** On choppy up days the brief's effect does show, and it is graded. The deepest third below the 20-day high falls −0.90 % the next day (t −2.14, 209 cases on 151 days), the middle third −0.48 % (t −1.89), and the shallowest third rises +0.16 % (t 0.37). Over two days the spread widens to −1.15 % (t −2.04) against +1.07 % (t 2.20). The finer split agrees: the deepest choppy up-day quintile is −1.01 % (t −2.04).
- **F3:** Outside choppy markets the same up-day fade is strongest in a falling 60-day trend, where the deepest tercile is −1.08 % (t −2.14, 510 cases on 173 days). In a rising trend the deepest tercile is +0.27 %. This is the falling bounce fade the map already holds (074-01 family), so it is not new.
- **F4:** Where the close sits in the day's range predicts the next day in reverse. Per unit of close position the next-day slope is −1.21 % (t −2.42, n 1,250) in choppy markets and −1.13 % (t −4.52, n 5,999) elsewhere. In choppy markets, up days closing in the top third of their range fall −0.62 % (t −2.11, 384 cases on 263 days). The per-coin rho is negative on 5 of 6 coins (−0.07 to −0.17; ETH 0.003), and the top tercile is negative in 2018–2020 and +0.09 % in 2021.
- **F5:** The day's own move, scaled by its 20-day swing, reverses outside choppy markets: slope −0.31 % per unit (t −4.54). The largest-fall quintile gains +0.70 % the next day (t 4.29). This is the fall-rebound family the map holds many times over.
- **F6:** Next-day excess returns swing by year, from −0.55 % (t −4.10) in 2018 to +0.44 % (t 3.19) in 2021. Weekday means range from −0.48 % to +0.42 %. These are drift and calendar noise that no idea explains, so they stay out of the ideas.
- **F7:** Depth sets the size of the book's trades, not their sign. The book's worst-gain quintile (−3.3 % per bar) and its best (+4.1 %) both sit at the deepest mean depth (−4.0 swings below the high), against about −2.3 in the middle quintiles.

## Ideas
- `072-03.g1_choppy-deep-up-day-fade` (from F2, F1, F7): In a choppy market, on a day that closed up, the further the close sits below the coin's 20-day high, in units of its 20-day daily-return standard deviation, the larger its fall over the next one to two days.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `072-03.g2_choppy-close-at-high-fade` (from F4): In a choppy market, the nearer a day's close sits to that day's high, as a share of the day's high-to-low range, the larger the coin's fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
