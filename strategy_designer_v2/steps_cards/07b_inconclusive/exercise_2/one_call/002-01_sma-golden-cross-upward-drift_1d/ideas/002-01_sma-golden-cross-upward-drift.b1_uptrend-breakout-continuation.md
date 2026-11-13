---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: For one coin whose 50-day SMA is above its 200-day SMA, a daily close at a new 20-day high is followed by a 10-day return above that coin's usual 10-day return.
Consequence: Within a golden-cross uptrend, a trader would take longs only on closes at fresh 20-day highs, not on the cross itself or on the size of the spread.
Why:
- F3: The effect sits in the uptrend bars that also have recent momentum: while the 50-day SMA is above the 200-day, the past 10-bar return predicts the next 10-bar excess return (slope 0.124, t 3.53, n 762), and still does net of the market (slope 0.071, t 2.86); in flat-state bars it predicts nothing (slope -0.004, t -0.12).
- F4: In uptrend bars where the close is at its 20-bar high, the next 10 bars beat the coin's mean by +0.0685 (t 2.38, n 91, hit 0.54), while flat-state bars at a 20-bar high earn only +0.0072 (t 0.49).
- F7: Fresh crosses do not start a drift: blocks within 20 bars of the forecast turning positive earn -0.018 (t -1.43, hit 0.46), and a widening spread barely beats a narrowing one (+0.006 vs -0.004, both |t| < 0.6).
- F1: The test's measure finds nothing because the size of the spread carries no signal and is swamped by noise: the slope t is 0.37, mean excess 10-bar returns across forecast buckets range only from -0.0085 to +0.0105 against a standard deviation of 0.137–0.217, and the top bucket (15–20) earns +0.00004 (t 0.00).
