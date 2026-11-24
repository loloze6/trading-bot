---
line: 7.b inconclusive
backtest: 031-02.b2.a1_deep-fall-rebound-nineteen-coins_1d
idea tested: 031-02.b2.a1_deep-fall-rebound-nineteen-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4124 USD
---
## Findings
- **F1:** The test's result is close to zero rather than leaning either way. Its main measure is -0.71 % per case over 30 days, with t -0.20, from 85 cases on 35 days. It already used every coin and every fold the daily data holds, so there is no more data to add.
- **F2:** The depth of the 90-day fall does grade the rebound, and that is the idea's core. Among the 30-day cases, the unusual return falls as the scaled 90-day return falls: slope -0.173 per usual move, t -2.19 on 35 days; Spearman rho -0.247, p 0.023 over 85 cases.
- **F3:** The flat average hides opposite results at different depths, and most cases sit where the idea fails. Falls of 1 to 1.5 usual moves are 59 of the 85 cases and lose 4.4 % (t -1.31, 29 days). Falls of 1.5 to 2 gain +3.4 % (19 cases). Falls of 2 to 2.5 gain +24.2 % (t 2.50, 6 cases on 4 days). The deepest tercile gains +7.0 % (strength 0.29), while the shallowest loses 5.7 %.
- **F4:** The 30-day part of the forecast adds little. The forecast's rank against the outcome gives Spearman rho 0.125 (p 0.255), weaker than depth alone in F2. Raw 30-day return against the outcome gives a correlation of -0.11. The 18 cases whose last 30 days rose lose 5.7 % (t -1.50, 7 days), against +0.6 % for the other 67.
- **F5:** The rebound shows more clearly over 45 days than over 30. For the deeper half of falls, the unusual return is +10.5 % over 45 days (t 2.63, 29 cases on 13 days, strength 0.33). Over 30 days the same half gives +4.3 % (t 0.90, 43 cases on 22 days). The 45-day gain is positive in 4 of 5 years and in both coin groups: +7.5 % (t 2.12) on the six default coins and +17.2 % (t 2.07) on the others.
- **F6:** Year to year the 30-day effect swings with the market. Its mean is -8.7 % in 2019 and -8.1 % in 2025 but +11.3 % in 2023, and each year has only 5 to 10 case days. So the market's own moves drown the 30-day average at this sample size.

## Ideas
- `031-02.b2.a1.b1_depth-graded-ninety-day-fall-rebound` (from F2, F3, F4): The further a coin's 90-day return stands below its own usual 90-day move, measured against its own past volatility, the more its price rises over the next 30 days than its usual drift, the deepest falls rebounding the most.
- `031-02.b2.a1.b2_deep-fall-rebound-45-days` (from F2, F5, F6): The further a coin's 90-day return stands below its own usual 90-day move, measured against its own past volatility, the more its price rebounds over the next 45 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
