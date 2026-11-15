---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In the two to four weeks after a coin's 50-day SMA crosses its 200-day SMA, the coin's return over the next 10 days runs against the direction of the cross: below its average after an up-cross and above its average after a down-cross.
Consequence: A trader would refuse to chase a fresh moving-average cross in its first weeks and would instead expect a pullback against it.
Why:
- F5: The weeks right after a cross move against it. Days 11-30 after an up-cross give a 10-day excess return of -0.037 (t -2.60, n 89, hit rate 40%). Days 11-30 after a down-cross give +0.042 (t 2.53, n 73, hit rate 62%). The same pattern holds at 20 days (-0.068, t -2.67).
- F4: The effect is mixed across periods. The yearly 10-day slope is significantly negative in 2020 (t -2.22) and 2022 (t -2.42), and lies between -1.13 and 0.14 in every other year. Being above the 200-day average beat being below it in only 2018, 2022 and 2025.
