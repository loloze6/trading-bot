---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: For one coin whose 50-day SMA is above its 200-day SMA, a positive 20-day return at the close is followed by a 10-day return above that coin's usual 10-day return.
Consequence: A trader would hold golden-cross longs only while the last 20 days are up, rather than at all times above the cross.
Why:
- F5: Inside the uptrend the past 20-bar direction splits the outcome in two: after a positive 20-bar return the excess is +0.022 (t 2.07, n 361), after a negative one it is -0.017 (t -2.26, n 333); in the flat state the same split gives +0.0002 and -0.0037 (both |t| < 0.6).
- F3: The effect sits in the uptrend bars that also have recent momentum: while the 50-day SMA is above the 200-day, the past 10-bar return predicts the next 10-bar excess return (slope 0.124, t 3.53, n 762), and still does net of the market (slope 0.071, t 2.86); in flat-state bars it predicts nothing (slope -0.004, t -0.12).
- F6: The uptrend-plus-momentum effect holds across coins but not across years: top-quartile past-10 uptrend blocks are positive in 5 of 6 coins (BTC +0.036, t 2.03, hit 0.63), yet negative in 2018 (-0.075), 2021 (-0.010) and 2023 (-0.023).
