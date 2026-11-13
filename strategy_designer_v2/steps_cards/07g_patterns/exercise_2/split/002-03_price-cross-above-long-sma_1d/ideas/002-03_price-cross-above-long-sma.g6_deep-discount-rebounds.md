---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close is more than 15% below its 200-day SMA, the coin rises over the following 20 bars.
Consequence: A trader would treat deep discounts to the long average as long entries rather than as a reason to stand aside.
Why:
- F7: The filter failed in both bear years and in the bull years. In 2018 active bars had a 20-bar return of -17.0% against -7.0% for flat bars, and in 2022 -9.2% against -0.9%. In 2020 and 2021 flat (below-SMA) bars returned +16.0% and +12.4% over 20 bars, against +6.4% and +4.8% for active bars. Bars more than 15% below the SMA returned +2.8% on non-overlapping 20-bar samples (t=2.07, n=241).
- F5: Forward 20-bar returns rose with the forecast level, but only at the top. On non-overlapping samples they were -0.36% for forecast 0–5 (t=-0.20, n=111), +1.6% for 5–10, +2.7% for 10–15 and +8.1% for 15–20 (t=1.69, n=113). Flat bars (forecast 0) earned +2.57% (t=2.42, n=412), so being just above the SMA did worse than being below it.
