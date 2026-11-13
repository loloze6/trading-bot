---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-02_sma-death-cross-downward-drift
line: 7.b inconclusive
backtest: 002-02_sma-death-cross-downward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: For a coin other than BTC that is in its death-cross state, the coin's price over the next 10 days falls further than its usual 10-day move when BTC's own 50-day average is also below its 200-day average.
Consequence: A trader should short an altcoin's death cross only when BTC is in its own death cross.
Why:
- F7: For non-BTC coins, the short does better when BTC is also in its death-cross state: +0.0058 (t 0.75, hit 0.55, n 481). With BTC flat it gives −0.010 (t −0.98, hit 0.45, n 226). Against the market the two buckets are +0.0004 and −0.0042.
- F2: The market's own move drowns the result. Each case's 10-bar forward return correlates 0.82 with the same-day cross-coin mean return (R² 0.68). Grouped by BTC's forward direction, the short's excess is +0.086 (t 13.5, hit 0.85) when BTC fell and −0.076 (t −10.9, hit 0.22) when BTC rose.
- F3: Measured against the cross-coin market instead of holding, the short's excess is −0.0001 (t −0.03). No year exceeds |t| 0.70 on that basis (2018 −0.001, 2021 −0.010, 2024 −0.008). Against holding, the years split strongly: 2018 +0.037 (t 1.75), 2019 +0.016 (t 1.87) and 2022 +0.015 (t 1.50) against 2020 −0.079 (t −4.44) and 2021 −0.063 (t −2.54). So the yearly signs follow the market's direction, not the cross.
