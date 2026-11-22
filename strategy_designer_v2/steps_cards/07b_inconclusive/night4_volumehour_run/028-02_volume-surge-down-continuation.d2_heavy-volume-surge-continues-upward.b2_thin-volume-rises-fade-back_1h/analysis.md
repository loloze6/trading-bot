---
line: 7.b inconclusive
backtest: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b2_thin-volume-rises-fade-back_1h
idea tested: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b2_thin-volume-rises-fade-back
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4606 USD
---
## Findings
- **F1:** The tested short after thin-volume rises shows no effect. Step 5's main measure is a short-side unusual 4-hour return of +0.0047 % per case, with t 0.35 over 11,108 cases. That is a strength of 0.003 of the coin's usual 4-hour move of 1.62 %. The total move is -0.02 % against a cost of 0.11 % per trade, and the book's Sharpe is -1.93.
- **F2:** The effect is not graded with the forecast, despite step 5's tiny positive slope (7.2e-06). On the forecast-active grid bars (forecast ≤ -2), the short-side 4-hour return by forecast size runs +0.032 % (t 0.88, n 1381) for 2–5, -0.050 % (t -1.06, n 833) for 5–10, -0.097 % (t -1.34, n 389) for 10–15 and +0.036 % (t 0.60, n 737) for 15–20.
- **F3:** No other horizon shows the fade either. After thin-volume rises above 2 typical hourly moves, the continuation is -0.005 % at 1 hour (t -0.23, n 1384), +0.063 % at 2 hours (t 1.53, n 712), -0.079 % at 4 hours (t -0.97, n 336), +0.063 % at 6 hours (t 0.56, n 235) and -0.015 % at 12 hours (t -0.06, n 122). The sign alternates and every |t| is below 2.
- **F4:** The sign flips across years and is held by no single period. The short-side 4-hour return on the forecast-active grid bars is +0.161 % in 2025 (t 2.50, n 441), but -0.110 % in 2020 (t -1.85, n 424) and -0.087 % in 2022 (t -1.18, n 431). By coin, BTC is -0.051 % (t -0.46, n 143) and ETH is -0.100 % (t -0.87, n 193) for the thin rises above 2 typical moves.
- **F5:** No regime isolates the effect clearly. After a 7-day fall the return is +0.047 % (t 1.33, n 1661), against -0.052 % (t -1.52, n 1679) after a 7-day rise. In low volatility it is +0.071 % (t 1.14, n 487), against -0.067 % (t -0.76, n 298) in high volatility. By hour of day it ranges from -0.031 % (t -0.68) to +0.043 % (t 1.05).
- **F6:** The brief's own heavy-volume continuation is not clear either. After hours above 3 typical moves on volume above 2.5 times average, the continuation is +0.016 % at 4 hours (t 0.16, n 794) and +0.274 % at 6 hours (t 1.73, n 471). By side, the 6-hour continuation is +0.316 % after rises (t 1.68, n 241) and +0.230 % after falls (t 0.89, n 230). Its yearly results swing from -0.384 % in 2021 to +0.751 % in 2025 (t 2.69, n 52).

## Ideas
- No ideas: The tested result is zero (t 0.35 on 11,108 cases, strength 0.003), and BTC and ETH were already tested over all four folds, so there is no more data for these coins. No coin, side, horizon, forecast size, year or regime shows the fade clearly while lacking it elsewhere (F2–F5), so the clear answer is that thin-volume hourly rises carry no fade.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
