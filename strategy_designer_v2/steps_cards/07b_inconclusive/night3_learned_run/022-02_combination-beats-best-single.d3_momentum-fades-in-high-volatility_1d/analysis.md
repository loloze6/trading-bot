---
line: 7.b inconclusive
backtest: 022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility_1d
idea tested: 022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3274 USD
---
## Findings
- **F1:** The effect shows at every horizon shorter than the plan's and weakens at the plan's 20 days. The main measure (forecast/10 × excess return, non-overlapping grid, 6 coins pooled) has t 3.1 at 3 days (5,723 cases), 2.6 at 5 days (3,419), 2.5 at 10 days (1,691) and 2.8 at 15 days (1,115), against 0.57 at 20 days (827) and 0.14 at 40 days (395). The bare sign of the 28-day return follows the same pattern: t 2.4 at 15 days, -0.07 at 20 days.
- **F2:** Where it shows, the idea's own volatility condition carries the effect. At 5 days the calmest third of 30-day against 90-day volatility gives a main-measure mean of 0.0256 (t 4.2, 564 cases), the most volatile third 0.0014 (t 0.26). At 10 days the calmest third gives 0.042 (t 3.0, 276 cases), the most volatile 0.003 (t 0.27).
- **F3:** The idea's move covers a trade at 10 to 15 days and not at 20. Per active case the unusual move is 0.63 % at 10 days (strength 0.044, about 3.3 times the 0.19 % round trip) and 1.16 % at 15 days (strength 0.060, about 6 times), against -0.03 % at 20 days. Step 5 measured -0.44 % at 20 days, -2.3 times the cost.
- **F4:** The effect is mixed over time. It is negative in w1-6 at every horizon (t -2.3 at 20 days, -1.7 at 5 and at 10 days) and positive in later windows: w13-18 at 5 days t 2.7, w19-24 at 10 days t 2.7 and at 20 days t 1.7.
- **F5:** The effect is graded in the forecast's size and spread over coins and sides.
- **F6:** The 20-day result is positive but weak (mean 0.0066, t 0.57) on 827 cases from 6 coins. The rise in t at shorter horizons comes from more independent cases and a cleaner move, which points to too little data at 20 days rather than no effect.

## Ideas
- `022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility.b1_calm-momentum-over-ten-days` (from F1, F2, F3, F5): The higher a coin's 28-day return, the higher its return over the next 10 days, the more so the lower its 30-day volatility is against its own past.
- `022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility.b2_calm-momentum-more-coins` (from F4, F6): The higher a coin's 28-day return, the higher its return over the next 20 days, the more so the lower its 30-day volatility is against its own past.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
