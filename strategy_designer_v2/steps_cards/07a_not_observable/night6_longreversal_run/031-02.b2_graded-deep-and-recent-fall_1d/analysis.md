---
line: 7.a not observable
backtest: 031-02.b2_graded-deep-and-recent-fall_1d
idea tested: 031-02.b2_graded-deep-and-recent-fall
step 5: not observable
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3106 USD
---
## Findings
- **F1:** The test found 52 cases on 29 distinct days against the plan's minimum of 30 distinct days, so it missed observability by a single day; on those cases the mean excess 30-day return was +0.02 % with t 0.006.
- **F2:** The 30-day horizon is about a quarter of each window: windows hold 119 to 123 daily bars, which gives 3 to 4 grid cells per window, 514 coin-cells in all and only about 95 distinct grid dates over 2018–2025. Distinct case days therefore cannot exceed about 95, however many coins are run.
- **F3:** Cases are only partly shared across coins: a case day has 1.79 active coins on average, 14 of the 29 case days had a single coin, and only 2 days had 5 coins. Each added coin can bring new case days, not just more cases on days already counted.
- **F4:** The situation is concentrated in a few periods.
- **F5:** The situation is reached more often by smaller coins: the share of bars with a positive forecast runs from 6.4 % for BTC and 7.0 % for ETH up to 12.0 % for XRP and 16.8 % for ZEC. Cases per coin run from 5 for BTC to 14 for ZEC.
- **F6:** The outcome varies widely from case to case: the excess 30-day return has a standard deviation of 20.7 % around a mean of +0.02 %, with a range from −48 % to +55 %. Even past the minimum, a clear reading needs many more independent days. Step 5's size measure, on 90 cases over 70 days, gave +9.05 % with t 1.71.

## Ideas
- `031-02.b2.a1_deep-fall-rebound-nineteen-coins` (from F1, F2, F3, F4, F5, F6): The further a coin's 90-day return stands below its own usual 90-day move, measured against its own past volatility, the more its price rebounds over the next 30 days, and the rebound is larger the further its last 30-day return also stands below zero.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
