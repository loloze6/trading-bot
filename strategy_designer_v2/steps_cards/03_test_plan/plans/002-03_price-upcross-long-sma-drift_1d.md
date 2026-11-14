---
idea: 002-03_price-upcross-long-sma-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: price has just closed above its long average after being below it -> adapted: "after the cross" becomes "while the close is above its 200-day SMA", graded by percent distance.
- Comparison: versus random points -> adapted: versus holding the coin over the same bars, which equals the average of random points.
- Outcome: price keeps rising over the following bars -> kept: forward return of the coin, long side.
- Verdict transfer: yes: forward gains that grow with the distance above the 200-day SMA, beyond the coin's own drift, confirm persistence after an up-cross, and their absence or reversal rejects it.
Forecast: The forecast is the percent distance of the daily close from its 200-day simple average. It is standardised against its own last 200 values (target 10, cap 20), then clipped at 0. It is positive and grows the further the close sits above the average. It is zero while the close is at or below the average. It is never short.
Config: 002-03_price-upcross-long-sma-drift_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Slope (with intercept) of the coin's next-10-bar log return on the forecast at the start of each block. Blocks are non-overlapping, pooled over all 6 windows, and costs are ignored. The intercept absorbs the coin's average drift, so the slope is the gain beyond holding the coin.
- Supporting check: Share of positive 10-bar returns in blocks with forecast > 0, against the share over all blocks.
- Confirm: Slope t-stat ≥ 2, with the supporting share higher in forecast > 0 blocks than in all blocks.
- Reject: Slope t-stat ≤ -2, meaning moves above the average reverse.
- Inconclusive: A t-stat between -2 and 2. It is also inconclusive if fewer than 50 non-overlapping blocks exist in total, or fewer than 20 of them start with forecast > 0.
