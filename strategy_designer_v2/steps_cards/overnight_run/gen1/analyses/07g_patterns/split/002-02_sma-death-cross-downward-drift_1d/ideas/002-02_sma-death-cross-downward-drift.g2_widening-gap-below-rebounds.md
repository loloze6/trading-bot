---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-02_sma-death-cross-downward-drift
line: 7.g patterns
backtest: 002-02_sma-death-cross-downward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While the 50-day SMA is below the 200-day SMA, a stretch where the spread widened downward over the past 10 days is followed by price rising over the next 10 days.
Consequence: A trader would buy into an accelerating downtrend gap below the long average instead of adding to shorts there.
Why:
- F4: While short, a widening spread is followed by rebounds. When the spread fell over the past 10 bars, the forward 10-bar return is +1.91% (t 2.75, 4376 bars), against +0.48% (t 0.73) when the spread was rising.
- F1: The bars do not drift down while the 50-day SMA is below the 200-day SMA; they drift up. Across all six coins the mean forward 10-bar return in the short state is positive: BTC +0.89%, ETH +0.57%, LTC +0.89%, XMR +1.05%, XRP +2.72%, ZEC +1.50%. The share of rising cases is 0.51–0.55, and for LTC and XMR the short state outpaces the non-short state (LTC +0.89% vs −0.25%, XMR +1.05% vs +0.84%).
