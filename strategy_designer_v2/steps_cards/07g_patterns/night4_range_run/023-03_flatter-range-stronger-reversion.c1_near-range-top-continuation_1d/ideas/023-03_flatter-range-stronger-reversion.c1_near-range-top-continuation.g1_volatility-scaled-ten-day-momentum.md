---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 10-day return relative to its own recent daily volatility, the more the coin rises over the following 10 days.
Consequence: A coin that has risen strongly over 10 days for its volatility is a reason to be long for the next 10 days, and one that has fallen strongly is a reason not to buy it.
Why:
- F1: Over the next 10 days, a coin's 10-day return scaled by its 20-day daily volatility predicts its excess return better than the range position does. Pooled, the slope is 0.094 of the coin's usual 10-day move per unit of z, with t 3.62 over 1403 non-overlapping cases. Fitted together with the 30-day range position and the 30-day z, the 10-day z keeps a coefficient of 0.155 (t 3.70), while the range position falls to −0.104 (t −1.27) and the 30-day z to 0.011 (t 0.27).
- F4: The 10-day continuation does not come from the last day. With the last day split out, the prior 9-day z has a coefficient of 0.088 (t 3.30) against 0.019 (t 0.76) for the last day's z. Measured from one day after the signal, the 9-day z still has 0.058 (t 2.17).
- F5: The 10-day continuation is uneven across years and coins, so it is not settled. Across years the slope ranges from −0.059 in 2022 to +0.266 (t 3.45) in 2020 and +0.151 (t 2.51) in 2024, and it is positive in all six coins (XRP 0.183, t 2.96; LTC 0.009). Across quintiles of the 10-day z, the next 10 days' excess return is −2.0 % in the second and third quintiles against +2.4 % (t 2.23) in the top quintile.
