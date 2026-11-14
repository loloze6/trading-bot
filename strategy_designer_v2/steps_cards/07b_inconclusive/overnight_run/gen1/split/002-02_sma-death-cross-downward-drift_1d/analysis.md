---
line: 7.b inconclusive
backtest: 002-02_sma-death-cross-downward-drift_1d
idea tested: 002-02_sma-death-cross-downward-drift
step 5: inconclusive
step 6: not profitable enough
mode: analyst then deducer
explorations: 2
cost: 0.3432 USD
---
## Findings
- **F1:** The short side's edge is tiny next to its noise: over 825 non-overlapping short cases the |forecast|-weighted excess gain is 0.0022 per 10 bars, its standard deviation is 0.137 and its t is 0.39. Its hit rate is 0.52 and its median is 0.0061.
- **F2:** The market's own move drowns the result. Each case's 10-bar forward return correlates 0.82 with the same-day cross-coin mean return (R² 0.68). Grouped by BTC's forward direction, the short's excess is +0.086 (t 13.5, hit 0.85) when BTC fell and −0.076 (t −10.9, hit 0.22) when BTC rose.
- **F3:** Measured against the cross-coin market instead of holding, the short's excess is −0.0001 (t −0.03). No year exceeds |t| 0.70 on that basis (2018 −0.001, 2021 −0.010, 2024 −0.008). Against holding, the years split strongly: 2018 +0.037 (t 1.75), 2019 +0.016 (t 1.87) and 2022 +0.015 (t 1.50) against 2020 −0.079 (t −4.44) and 2021 −0.063 (t −2.54). So the yearly signs follow the market's direction, not the cross.
- **F4:** Ranked by the raw SMA spread, the shallowest quartile (short average only just below the long one) loses: −0.025 (t −2.53, hit 0.45, n 206). The deepest quartile gains +0.0087 (t 0.76, hit 0.55). The middle quartiles are mixed (q2 −0.004, q3 +0.012).
- **F5:** The |forecast| terciles are not monotone: low −0.0053 (t −0.60), mid +0.0057 (t 0.67), high +0.0018 (t 0.21). The supporting check's top-minus-bottom pass (0.0071) therefore rests on the bottom tercile's loss, not on a strong top tercile.
- **F6:** Freshly crossed bars lose and older crosses gain slightly. Bars 0–20 after the cross give −0.022 (t −1.63, hit 0.46, n 227), 21–60 bars give +0.0037 (t 0.49) and 61–150 bars give +0.0094 (t 0.86). Against the market, every age bucket is about 0 (|t| < 0.09).
- **F7:** For non-BTC coins, the short does better when BTC is also in its death-cross state: +0.0058 (t 0.75, hit 0.55, n 481). With BTC flat it gives −0.010 (t −0.98, hit 0.45, n 226). Against the market the two buckets are +0.0004 and −0.0042.
- **F8:** No coin carries the effect. Every coin's |t| is ≤ 0.75 (ZEC +0.0098, BTC +0.0049, ETH +0.0047, XMR −0.0064, XRP −0.0014). Only 43.8% of 112 coin-windows have a positive mean short excess (mean −0.017).
- **F9:** Flat (forecast 0) bars have a forward return minus holding of +0.00015 (n 832), against −0.0012 on short bars. That is a 0.13-point difference over 10 bars. The 60-day momentum split also does not separate the short cases (down −0.0006, t −0.06; up +0.0037, t 0.51).

## Ideas
- `002-02_sma-death-cross-downward-drift.b1_shallow-fresh-death-cross-reversal` (from F4, F6, F5): In the first weeks after a coin's 50-day average crosses below its 200-day average, while the short average is still only just under the long one, the coin's price over the next 10 days rises more than its usual 10-day move.
- `002-02_sma-death-cross-downward-drift.b2_deep-established-death-cross-drift` (from F4, F6, F5): When a coin's 50-day average has sat well below its 200-day average for some time, after a deep and established death cross, the coin's price over the next 10 days falls further than its usual 10-day move.
- `002-02_sma-death-cross-downward-drift.b3_altcoin-death-cross-with-btc` (from F7, F2, F3): For a coin other than BTC that is in its death-cross state, the coin's price over the next 10 days falls further than its usual 10-day move when BTC's own 50-day average is also below its 200-day average.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
