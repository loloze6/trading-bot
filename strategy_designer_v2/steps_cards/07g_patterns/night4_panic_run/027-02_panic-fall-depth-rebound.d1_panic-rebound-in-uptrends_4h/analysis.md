---
line: 7.g patterns
backtest: 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends_4h
idea tested: 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3923 USD
---
## Findings
- **F1:** The 4h bar opening at 16:00 UTC rises more than any other bar of the day. Its next-bar return averages +0.099 % (t 6.64 over 17,506 bars). Every one of the six coins is positive on its own, from +0.069 % (BTC, t 2.67) to +0.154 % (ZEC, t 3.53). All eight years are positive, five of them with t above 2 (2021 +0.198 %, t 3.71; 2024 +0.137 %, t 4.00). With this many angles checked, it is the one pattern that clearly stands out.
- **F2:** The 16:00 UTC rise grows with the coin's 30-day volatility. By tercile of the coin's own volatility it is +0.048 %, +0.067 % and +0.133 %. Measured in the coin's own bar volatility it stays roughly constant (0.050, 0.034, 0.053), so it is a fixed share of a usual move, which matches the ~0.05 strength of real ideas. It is still below the 0.19 % cost of a trade, so it cannot pay as a standalone round trip.
- **F3:** Fridays are positive overall (+0.101 % per 4h bar, t 6.20, all six coins positive, t 1.89 to 4.04), but the effect is not stable. It fades or turns in 2021 (+0.067 %, t 1.11), 2022 (−0.057 %, t −1.47) and 2025 (−0.003 %). It is spread over all six hours of the day rather than concentrated in one.
- **F4:** The 20:00 UTC bar is negative on average (−0.049 %, t −3.18), but its sign flips across years: −0.280 % in 2018 (t −5.04) against +0.095 % in 2024 (t 2.56). It is not a stable pattern.
- **F5:** In the tested panics (24h range at least 2.5 times its 30-day mean), falls are followed over the next 24h by +2.05 % (t 2.04, 40 cases) and rises by +1.05 % (t 0.31, 12 cases). Given how many angles were checked, this is not distinguishable from chance.
- **F6:** The depth of the panic fall does not grade the 14-day outcome. By quartile of the fall, in usual 24h moves, the unusual 14-day return is +4.9 %, −0.7 %, +9.1 % and +2.2 % (about 13 cases each). Across all 720 non-overlapping 14-day cells, the slope of the unusual return on the log range ratio is 0.024 with t 1.42. The top range quintile gives +3.04 % with t 1.40.
- **F7:** Panic falls of ratio at least 3 nearly all come with a negative 30-day return: 23 of 25 cases, +2.58 % unusual over 14 days, t 1.03. So the tested idea's "positive 90-day return" condition leaves very few cases. That sparsity matches the book's failed trade count (0.0094 trades a day).

## Ideas
- `027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends.g1_afternoon-utc-volatility-scaled-rise` (from F1, F2): Over the four hours from 16:00 to 20:00 UTC, a coin rises more than in its other hours of the day, and the higher its 30-day volatility, the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
