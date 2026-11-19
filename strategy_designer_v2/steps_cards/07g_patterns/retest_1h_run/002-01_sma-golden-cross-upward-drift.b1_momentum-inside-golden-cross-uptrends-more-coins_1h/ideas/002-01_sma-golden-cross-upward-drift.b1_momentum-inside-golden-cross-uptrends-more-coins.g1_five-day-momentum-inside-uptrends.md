---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins
line: 7.g patterns
backtest: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1h
period: folds A, B, C, D
---
Idea: While a coin's 50-day SMA is above its 200-day SMA, the higher its own 5-day return, the larger its return over the next 10 days.
Consequence: Inside an uptrend, a trader should scale long exposure by the last 5 days' move rather than the last 20, and refuse longs in uptrends whose last 5 days fell hardest.
Why:
- F1: Inside the `trending` regime, on the 240-bar grid, the coin's 5-day return carries the whole forecast and the tested 20-day return adds nothing once both are in the same regression: 5-day slope 0.362 with t 7.36, 20-day slope 0.017 with t 0.92, n 1285.
- F2: The 5-day return grades the next 10 days' excess return in `trending`, but mostly at the extremes: the top 5-day quintile is followed by +6.44% (t 3.40, n 284), the bottom by -3.52% (t -4.49), and the middle three sit between -1.3% and -0.8%.
- F3: The 20-day momentum the idea uses works only inside the regime: outside `trending` its slope on 10-day excess return is -0.0020 (t -0.11, n 1305), and the 5-day slope drops from 0.35 (t 8.59, n 1421) in `trending` to 0.081 (t 2.37, n 1437) outside it.
- F4: The 5-day effect in `trending` is not steady across years: slopes are positive in 2020 (t 2.20), 2021 (t 5.10), 2024 (t 5.04) and 2025 (t 3.83), but negative or near zero in 2018 (t -0.83), 2019 (t -0.00), 2022 (t -1.68) and 2023 (t -0.63), so it rests on the bull years.
