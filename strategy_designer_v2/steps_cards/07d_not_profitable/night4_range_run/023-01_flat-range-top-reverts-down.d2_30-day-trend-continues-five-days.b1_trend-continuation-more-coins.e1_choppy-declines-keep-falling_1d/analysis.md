---
line: 7.d not profitable
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e1_choppy-declines-keep-falling_1d
idea tested: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e1_choppy-declines-keep-falling
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4568 USD
---
## Findings
- **F1:** The book fails on its gain. Its mean daily return is -0.0066 % a coin-day, and -0.0053 % before fees. Holding's own rise takes -0.0108 % a day, because the book is short on 52 % of days in coins whose normal 5-day drift is positive for all 19 coins. Timing adds back only +0.0043 %. The total move per case is +0.13 %, 0.6 times the 0.22 % cost of a trade.
- **F2:** The forecast's strength does not grade the move. Grid short bars by forecast quartile, strongest to weakest, give total moves of +0.19 %, +0.43 %, -0.14 % and -0.08 % (t 0.35, 0.91, -0.28, -0.17, about 464 cases each). Trades lose in every entry-forecast quartile, from -0.99 % to -3.12 % net, over 3225 trades.
- **F3:** Losses come from sharp rebounds against the short. The book's daily returns correlate -0.56 with the coin. The coin rose +14.0 % on average on the book's worst 1 % of days, and those days sum to 3.8 times the book's whole net result. The worst 5 % of trades lose 26.6 % or more, and the trade mean is -2.0 % with them but +1.05 % without them.
- **F4:** The fall pays where the coin closes high in its 30-day range. In the top quartile of position in the 30-day high-low range (above 0.51), the total move is +1.64 % (t 3.02) and the unusual move +2.42 % (t 4.44), over 339 cases. The three lower quartiles give total moves of +0.37 %, -0.19 % and -0.27 %.
- **F5:** The fall pays after a recent bounce. When the coin's prior 5-day return is in its top quartile (above +5.35 %), the total move is +1.14 % (t 2.23) and the unusual move +1.96 % (t 3.82), over 444 cases. The other quartiles give total moves of -0.30 %, -0.07 % and -0.19 %.
- **F6:** The fall pays more when volatility is high and rising. In the top quartile of 30-day volatility, the total move is +1.56 % (t 2.59), against -0.45 % in the bottom quartile. In the top quartile of 30-day over 60-day volatility, it is +1.78 % (t 2.79).
- **F7:** After the deepest 60-day falls (below -29.5 %), the short loses: the total move is -1.07 % (t -1.35, 215 cases), against +0.68 % to +0.96 % in the other quartiles.

## Ideas
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e1_choppy-declines-keep-falling.d1_choppy-decline-high-in-range` (from F1, F2, F3, F4): In a coin that has fallen over the past 30 days while its 30-day net move stayed small against its 30-day high-low range, the higher its close sits within that 30-day range, the further the coin falls over the next 5 days.
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e1_choppy-declines-keep-falling.d2_bounce-inside-choppy-decline` (from F1, F2, F5): In a coin that has fallen over the past 30 days while its 30-day net move stayed small against its 30-day high-low range, the larger its rise over the past 5 days, the further the coin falls over the next 5 days.
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e1_choppy-declines-keep-falling.d3_choppy-decline-rising-volatility` (from F1, F2, F6): In a coin that has fallen over the past 30 days while its 30-day net move stayed small against its 30-day high-low range, the further the coin keeps falling over the next 5 days, the higher its 30-day volatility stands against its 60-day volatility.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
