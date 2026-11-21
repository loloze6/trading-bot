---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.d2_jump-rises-continue-less
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.d2_jump-rises-continue-less_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: In the evening hours just after 21:00 UTC, the higher a coin's realised volatility of hourly returns over the past 24 hours, the larger its rise over the next 2 hours.
Consequence: A trader would lean long into the late-UTC evening hours, and more so after volatile days, instead of buying at a random hour.
Why:
- F3: The 1-hour bars starting at 20:00 and 21:00 UTC rise more than all other hours in every coin, by 0.00041 to 0.00053 per bar (t 2.66 to 4.10, about 5,800 bars per coin). The effect is positive in 7 of 8 years (t up to 4.95 in 2024); the exception is 2022 (-0.00017, t -1.07).
- F4: After the bar starting at 20:00 UTC, the next 2-hour return grows with the coin's 24-hour volatility of hourly returns. By volatility quintile it rises from +0.00037 (t 3.00) in the calmest to +0.00076, +0.00098 and +0.00257 (t 6.64) in the most volatile, with about 3,450 cases each. Ranked instead by the prior 20-hour return, the same 2-hour return is positive in every quintile and shows no order.
- F5: The book never trades the evening drift: the bar-level hour effect (F3, F4) is untouched by a 72-hour long-only forecast.
