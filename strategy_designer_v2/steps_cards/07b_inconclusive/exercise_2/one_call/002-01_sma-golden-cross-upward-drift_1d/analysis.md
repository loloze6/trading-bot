---
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
idea tested: 002-01_sma-golden-cross-upward-drift
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3009 USD
---
## Findings
- **F1:** The test's measure finds nothing because the size of the spread carries no signal and is swamped by noise: the slope t is 0.37, mean excess 10-bar returns across forecast buckets range only from -0.0085 to +0.0105 against a standard deviation of 0.137–0.217, and the top bucket (15–20) earns +0.00004 (t 0.00).
- **F2:** Market moves drown much of the coin-level outcome: a coin's 10-bar return correlates 0.757 with the all-coin mean for the same block, and that common move carries about 57% of the return variance (0.0144 of 0.0251).
- **F3:** The effect sits in the uptrend bars that also have recent momentum: while the 50-day SMA is above the 200-day, the past 10-bar return predicts the next 10-bar excess return (slope 0.124, t 3.53, n 762), and still does net of the market (slope 0.071, t 2.86); in flat-state bars it predicts nothing (slope -0.004, t -0.12).
- **F4:** In uptrend bars where the close is at its 20-bar high, the next 10 bars beat the coin's mean by +0.0685 (t 2.38, n 91, hit 0.54), while flat-state bars at a 20-bar high earn only +0.0072 (t 0.49).
- **F5:** Inside the uptrend the past 20-bar direction splits the outcome in two: after a positive 20-bar return the excess is +0.022 (t 2.07, n 361), after a negative one it is -0.017 (t -2.26, n 333); in the flat state the same split gives +0.0002 and -0.0037 (both |t| < 0.6).
- **F6:** The uptrend-plus-momentum effect holds across coins but not across years: top-quartile past-10 uptrend blocks are positive in 5 of 6 coins (BTC +0.036, t 2.03, hit 0.63), yet negative in 2018 (-0.075), 2021 (-0.010) and 2023 (-0.023).
- **F7:** Fresh crosses do not start a drift: blocks within 20 bars of the forecast turning positive earn -0.018 (t -1.43, hit 0.46), and a widening spread barely beats a narrowing one (+0.006 vs -0.004, both |t| < 0.6).

## Ideas
- `002-01_sma-golden-cross-upward-drift.b1_uptrend-breakout-continuation` (from F3, F4, F7, F1): For one coin whose 50-day SMA is above its 200-day SMA, a daily close at a new 20-day high is followed by a 10-day return above that coin's usual 10-day return.
- `002-01_sma-golden-cross-upward-drift.b2_uptrend-with-recent-momentum` (from F5, F3, F6): For one coin whose 50-day SMA is above its 200-day SMA, a positive 20-day return at the close is followed by a 10-day return above that coin's usual 10-day return.
- `002-01_sma-golden-cross-upward-drift.b3_uptrend-pullbacks-keep-falling` (from F5, F3): For one coin whose 50-day SMA is above its 200-day SMA, a negative 20-day return at the close is followed by a 10-day return below that coin's usual 10-day return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
