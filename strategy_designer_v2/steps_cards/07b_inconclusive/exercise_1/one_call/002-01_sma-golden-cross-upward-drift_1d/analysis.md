---
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
idea tested: 002-01_sma-golden-cross-upward-drift
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2864 USD
---
## Findings
- **F1:** The forecast's size carries no information: mean excess 10-bar returns by forecast bucket are -0.85% (0–5, t=-0.82), +0.23% (5–10, t=0.17), +1.05% (10–15, t=0.64) and +0.004% (15–20, t=0.00), against -0.05% when flat, and the raw-spread quintiles run from +0.54% to -0.73% with no |t| above 0.71, so the pooled slope (t=0.37) averages over nothing.
- **F2:** Inside the active state (50-day SMA above 200-day), the past 20-day return splits the outcome: when it is positive the next 10 bars beat the coin's mean by +2.14% (n=361, t=2.00), and when it is negative they fall short by -1.78% (n=333, t=-2.36). With the same split on flat bars the results are -0.47% and -0.07% (|t|≤0.65).
- **F3:** Within active bars, excess forward return rises with the past 20-day return (slope 0.102, t=3.61, n=694), while on flat bars it does not (slope -0.020, t=-0.81). Across past-20 quintiles the excess runs from -3.19% (t=-2.57) in the weakest to +3.96% (t=1.76) in the strongest.
- **F4:** Active bars where the close is below its 50-day SMA are followed by -3.23% excess over 10 bars (n=205, t=-3.62), versus +0.68% (n=288, t=0.62) when the close is above it. The past 10-day sign gives the same split: -1.87% (t=-2.38) when down and +2.35% (t=2.22) when up.
- **F5:** The effect depends heavily on the period, which drowns it in the pooled test. The active, up-20 case earns +4.6% (t=2.37) in 2020 and +7.8% (t=2.40) in 2021 but -3.8% (t=-4.21) in 2023, and over all bars the yearly excess swings from -4.6% (2018, t=-3.20) to +2.7% (2020, t=2.44).
- **F6:** Fresh crosses do not start trends: in the first 20 days after the 50-day SMA turns above the 200-day, the excess return is -1.80% (n=107, t=-1.43), and its share of positive returns is 5.2 points below the coin's.
- **F7:** Positive medians are rare even where the means are positive. The active, up-20 case has a median excess of -1.37% overall and is positive by median only for ETH (+0.97%) and ZEC (+1.24%), so a few large up-moves drive the means.

## Ideas
- `002-01_sma-golden-cross-upward-drift.b1_golden-cross-with-momentum` (from F2, F3, F4, F5, F7): In a coin whose 50-day SMA is above its 200-day SMA, and whose close is higher than 20 days earlier, the close 10 days later sits further above the current close than the coin's typical 10-day move.
- `002-01_sma-golden-cross-upward-drift.b2_golden-cross-pullback-weakness` (from F2, F4): In a coin whose 50-day SMA is above its 200-day SMA but whose close has fallen below its 50-day SMA, the close 10 days later is lower relative to the current close than the coin's typical 10-day move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
