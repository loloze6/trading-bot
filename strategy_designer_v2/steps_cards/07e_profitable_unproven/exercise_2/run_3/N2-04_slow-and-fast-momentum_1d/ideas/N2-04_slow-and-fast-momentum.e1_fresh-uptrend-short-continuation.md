---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-04_slow-and-fast-momentum
line: 7.e profitable but not proven
backtest: N2-04_slow-and-fast-momentum_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin's medium and slow returns have both just turned positive, its price keeps rising faster than its usual pace over the following days to two weeks, and the younger that joint up-trend is, the larger the extra rise.
Consequence: A trader should buy a coin early in a fresh joint up-turn and hold for days rather than a month, and should not add exposure to an up-trend that has run for several weeks.
Why:
- F1: The book's timing part is twice its market part: of a mean daily book return of 0.000754 (Sharpe 1.055), 0.000503 is timing and 0.000252 comes from the coins' own rise. On the days it holds a coin, that coin returns 0.002937 a day, against 0.000311 on the days it is out (5816 against 11564 coin-days).
- F2: The idea's excess return on active bars is real at short horizons and fades by the plan's 20 bars. Mean excess over the coin's mean, non-overlapping, by horizon:
- F3: The gain sits in young up-trends. In the first 0–10 bars of the trending regime, the 5-bar excess is 0.0113 (t 2.20, n 593) and the 10-bar excess is 0.0263 (t 2.46, n 298). Trends 31–60 bars old give -0.0038 at 5 bars and -0.0170 at 10 bars.
- F4: The book's profit is concentrated, but it is not a few-trades artefact of one coin:
