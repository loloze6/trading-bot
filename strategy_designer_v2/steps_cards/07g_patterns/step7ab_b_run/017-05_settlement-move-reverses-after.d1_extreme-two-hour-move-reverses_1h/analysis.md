---
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d1_extreme-two-hour-move-reverses_1h
idea tested: 017-05_settlement-move-reverses-after.d1_extreme-two-hour-move-reverses
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4041 USD
---
## Findings
- **F1:** The coin's 1-day fall carries a rebound that the tested idea dilutes. On a non-overlapping 24-hour grid (all 6 coins, 15,662 cases), the 10 % of cases with the deepest 24-hour fall, measured in usual 24-hour moves (mean z -1.74), rose +78.6 bps more than the coin's drift over the next 24 hours (t 4.90, n 1567). They rose +93.2 bps over 72 hours (t 4.13). That is about 4 times the 19 bps round trip this backtest applied.
- **F2:** The rebound is graded and convex in the depth of the fall:
- **F3:** The rebound after deep falls is positive on all 6 coins over 24 hours: XRP +136 bps (t 3.10), ZEC +132 (t 2.73), XMR +91 (t 2.04), ETH +59 (t 1.78), LTC +37 (t 0.93), BTC +31 (t 1.20). It is larger on the costlier, more volatile coins.
- **F4:** The rebound is concentrated in a few periods: 2018 +210 bps (t 4.37) and 2021 +272 bps (t 4.26), while 2019, 2022 and 2024 are near 0. By window quarter, w13–w18 gives +195 bps (t 4.31) and w19–w24 +22.5 (t 0.82). The rebound is regime-dependent, not steady.
- **F5:** Rises do not mirror falls, which is one reason the symmetric fade loses:
- **F6:** Other patterns stood out but are not usable here:

## Ideas
- `017-05_settlement-move-reverses-after.d1_extreme-two-hour-move-reverses.g1_deep-daily-fall-rebounds` (from F1, F2, F3, F4, F5): The deeper a coin's fall over the past day relative to its usual 1-day move, the more it rises above its normal drift over the next 1 to 3 days, with the rebound growing fastest for the deepest falls.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
