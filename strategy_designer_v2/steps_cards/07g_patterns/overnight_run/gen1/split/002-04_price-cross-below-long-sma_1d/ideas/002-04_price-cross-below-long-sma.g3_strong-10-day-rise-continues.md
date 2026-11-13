---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.g patterns
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's past-10-day return is in its top fifth (above about +10%), it tends to keep rising over the next 10 bars, both above and below its 200-day average.
Consequence: A trader would go long after a strong 10-day rise, and would close or refuse shorts when that rise happens below the long average.
Why:
- F3: Short-term momentum carries forward on both sides of the SMA. Bars in the top quintile of past-10-day return (> +10.4%) are followed by +3.86% over 10 bars (t 10.49), against +0.26% to +0.47% for the bottom three quintiles. Within the top quintile, the forward return is +4.35% (t 8.94) above the SMA and still +2.73% (t 5.81, 57.8% up) below it.
- F8: The book's worst days follow sharp upside reversals while it is deeply short. On its 171 worst days (mean book return -19.3%), the coin rose +12.7% that day, with mean allocation -1.31 and SMA distance -32%. Its 171 best days came on -11.1% coin days after a -21.7% 10-day slide, at distance -46%.
- F12: The book loses in most years, and 2018 is the only one positive on average. Mean daily book return is +0.16% in 2018, -0.31% in 2020 (t -4.30) and -0.10% in 2021 (t -3.65). In 2020 and 2021 the coin's next-day return while the book was short was +0.72% (t 3.86) and +0.68% (t 3.39), higher than while flat.
