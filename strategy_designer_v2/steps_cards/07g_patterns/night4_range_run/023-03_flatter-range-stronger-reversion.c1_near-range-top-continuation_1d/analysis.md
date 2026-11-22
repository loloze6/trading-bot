---
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation_1d
idea tested: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5637 USD
---
## Findings
- **F1:** Over the next 10 days, a coin's 10-day return scaled by its 20-day daily volatility predicts its excess return better than the range position does. Pooled, the slope is 0.094 of the coin's usual 10-day move per unit of z, with t 3.62 over 1403 non-overlapping cases. Fitted together with the 30-day range position and the 30-day z, the 10-day z keeps a coefficient of 0.155 (t 3.70), while the range position falls to −0.104 (t −1.27) and the 30-day z to 0.011 (t 0.27).
- **F2:** After a large one-day move in a high-volatility coin, the next day tends to go the other way. In the top third of each coin's 20-day volatility, the next-day excess return has a slope of −0.134 standard deviations per unit of the one-day z, with t −7.39 over 4830 days. The same slope is +0.020 (t 1.89) in the low-volatility third, and −0.038 (t −4.61) pooled over 14500 days.
- **F3:** The one-day reversal is strongest after the largest falls. The bottom fifth of one-day z is followed by +0.39 % next-day excess return (t 4.04, 2900 days), which is twice the 0.19 % cost of a trade. It is negative in all eight years, with t ≤ −3 in 2018, 2020 and 2023, and negative in all six coins, ranging from −0.006 for ZEC to −0.093 for XMR (t −4.67).
- **F4:** The 10-day continuation does not come from the last day. With the last day split out, the prior 9-day z has a coefficient of 0.088 (t 3.30) against 0.019 (t 0.76) for the last day's z. Measured from one day after the signal, the 9-day z still has 0.058 (t 2.17).
- **F5:** The 10-day continuation is uneven across years and coins, so it is not settled. Across years the slope ranges from −0.059 in 2022 to +0.266 (t 3.45) in 2020 and +0.151 (t 2.51) in 2024, and it is positive in all six coins (XRP 0.183, t 2.96; LTC 0.009). Across quintiles of the 10-day z, the next 10 days' excess return is −2.0 % in the second and third quintiles against +2.4 % (t 2.23) in the top quintile.
- **F6:** The brief's reversion does not show in flat coins. In the flat half of the 30-day trend measure, the next 10 days' excess return is −0.39 % (t −0.39) at the bottom third of the range and +0.11 % (t 0.09) at the top third. The tested continuation also shows only in trending coins: +1.33 % (t 1.16) at the top third.
- **F7:** The book's gain sits in a few large days, and the longs carry it.
- **F8:** There is a weekday pattern in the next-day excess return, but it is not stable enough to act on. Next-day excess return after Thursday and Friday closes exceeds that after Monday and Wednesday closes by 1.76 % in 2019 (t 7.0), 0.77 % in 2024 (t 3.05) and 0.51 % in 2025 (t 2.0), but it turns negative in 2022 (−0.42 %, t −1.57). No idea is drawn from it, because a weekday is not a graded situation.

## Ideas
- `023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.g1_volatility-scaled-ten-day-momentum` (from F1, F4, F5): The larger a coin's 10-day return relative to its own recent daily volatility, the more the coin rises over the following 10 days.
- `023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.g2_high-volatility-one-day-reversal` (from F2, F3): When a coin's past 20 days have been highly volatile, the larger its one-day move relative to that volatility, the more the coin moves back the other way over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
