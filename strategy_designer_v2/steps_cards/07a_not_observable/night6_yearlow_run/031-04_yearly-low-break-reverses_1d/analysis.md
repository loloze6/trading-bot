---
line: 7.a not observable
backtest: 031-04_yearly-low-break-reverses_1d
idea tested: 031-04_yearly-low-break-reverses
step 5: not observable
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3779 USD
---
## Findings
- **F1:** The test found 13 cases on 12 distinct days against the plan's minimum of 20 cases on 15 days. Over about 46.7 coin-years of the six default coins, that is 0.28 cases per coin-year, so the default data cannot reach the minimum.
- **F2:** The situation itself is rare. Closes below the prior 365-day low occur on only 227 of about 17,000 coin-days (4.9 per coin-year), in 144 episodes with a median length of 1 day and a maximum of 6. 17 of the 24 windows hold 7 or fewer such bars, and 9 of them hold none.
- **F3:** Most breaks are too shallow to count as cases. On the 227 break days the forecast has a median of 0.13, and 196 of them sit at or below 1. Only 15 reach a forecast of 2 or more, the level a case needs.
- **F4:** The cases bunch in a few coins and years. ZEC gives 8 of the 13 cases from 71 of the 227 break bars. ETH and LTC give none from 41 and 37 break bars. 2021 has no break bar at all, and 2018 has 87 break bars but no case.
- **F5:** The outcome varies widely from case to case. The 13 cases' 10-day returns average +9.0 % with a standard deviation of 18.2 % and range from -15.8 % to +60.3 %. The forecasts behind them run from 2.1 to 10.1.
- **F6:** The idea's size would matter if it holds. Its unusual move of +7.15 % (t 1.47, 12 days) is 0.45 of the coin's usual 10-day move and 37 times the 0.19 % cost of a trade. The minimum count is the only thing that kept it from being read.
- **F7:** Adding the other 13 coins roughly doubles the coin-years. ADA, DOGE, LINK, TRX, UNI and AAVE add about 31 coin-years, AVAX, SOL and INJ about 12, and NEAR, SUI, TAO and ONDO about 8, for about 50 more before warm-up. At 0.28 cases per coin-year that gives about 14 more cases, for a total near 27, above the 20-case minimum. Alts in the 2022 and 2025 drawdowns likely add more than that rate.

## Ideas
- `031-04.a1_yearly-low-break-all-coins` (from F1, F2, F3, F4, F6, F7): When a daily close falls below the lowest close of the prior 365 days, the coin rises over the next 10 days. The further the close is below that old low, the larger the rebound.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
