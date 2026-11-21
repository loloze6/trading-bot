---
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.d2_jump-rises-continue-less_1h
idea tested: 016-03_up-jump-price-reversal.d2_jump-rises-continue-less
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5181 USD
---
## Findings
- **F1:** The book loses because its edge is smaller than its costs. Each bar it earns 0.000013 before fees and pays 0.000034 in fees, on a turnover of 0.037. About 0.000008 of the 0.000013 gross gain comes from the market's own rise, since the mean position is 0.13 and the book is long on only 22.7 % of bars. Its mean daily return is -0.000523 against the coins' +0.001179.
- **F2:** The tested pattern is real in rank but small and carried by few coins. Over 2865 risen 72-hour cases, the pooled Spearman correlation of the next 3-day excess return with the top-3-gain share is -0.056 (t -3.03). The lowest share quintile gains +0.0107 (t 2.75) and the highest loses -0.0061 (t -1.79). Per coin only ZEC reaches significance (t -2.51), and the per-coin linear slopes are all insignificant (t between -1.26 and +0.46).
- **F3:** The 1-hour bars starting at 20:00 and 21:00 UTC rise more than all other hours in every coin, by 0.00041 to 0.00053 per bar (t 2.66 to 4.10, about 5,800 bars per coin). The effect is positive in 7 of 8 years (t up to 4.95 in 2024); the exception is 2022 (-0.00017, t -1.07).
- **F4:** After the bar starting at 20:00 UTC, the next 2-hour return grows with the coin's 24-hour volatility of hourly returns. By volatility quintile it rises from +0.00037 (t 3.00) in the calmest to +0.00076, +0.00098 and +0.00257 (t 6.64) in the most volatile, with about 3,450 cases each. Ranked instead by the prior 20-hour return, the same 2-hour return is positive in every quintile and shows no order.
- **F5:** The book never trades the evening drift: the bar-level hour effect (F3, F4) is untouched by a 72-hour long-only forecast.
- **F6:** Other angles show nothing that stands out after this many looks:

## Ideas
- `016-03_up-jump-price-reversal.d2_jump-rises-continue-less.g1_volatile-day-evening-drift` (from F3, F4, F5): In the evening hours just after 21:00 UTC, the higher a coin's realised volatility of hourly returns over the past 24 hours, the larger its rise over the next 2 hours.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
