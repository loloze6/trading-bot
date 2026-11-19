---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin closes above its long moving average, the nearer its close sits to the top of its 20-day range and the stronger its 20-day rise, the larger its return over the following 14 days.
Consequence: A slow, monthly-range version of the momentum signal can carry the two-week drift while changing position about once every two days.
Why:
- F1: Fees, not a missing effect, sink the book. Before costs the positions earn +0.000084 per coin-day. Fees cost 0.001842 per coin-day on a turnover of 1.70 per day. That nearly matches the book's mean daily return of -0.001761 over 17381 coin-days, with a Sharpe of -3.21.
- F2: The forecast switches far too often for a two-week effect. It turns on or off 1.75 times a day across 15227 on-runs, with a median run of 3 hours and 52.9% of runs lasting 3 hours or less, so the book keeps paying to enter and leave.
- F3: The forecast's information sits only at the slow horizon. At 336 hours the top forecast tercile gains +0.0784 (n=140) against +0.0252 when the forecast is zero (n=215). At 24 hours the top tercile loses -0.0011 (n=1995) against +0.0038 for zero (n=2944). The hourly moves the book trades on carry no edge.
- F5: A slower measure keeps the two-week effect and needs far fewer switches. Rise times nearness to the high, over 168 bars (7 days), has a 336-bar excess-return slope t of 3.21 over 522 non-overlapping cases, with terciles of -0.0276, -0.0087 and +0.0284, and switches 0.81 times a day. Over 480 bars (20 days) the slope t is 2.91 over 432 cases, the top tercile is +0.0424, and it switches 0.55 times a day.
