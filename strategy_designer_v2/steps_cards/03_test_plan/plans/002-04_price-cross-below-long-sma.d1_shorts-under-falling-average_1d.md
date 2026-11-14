---
idea: 002-04_price-cross-below-long-sma.d1_shorts-under-falling-average
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: close below its 200-day SMA while that SMA is declining -> kept: a regime rule on the close's distance from SMA200 being below 0, and the SMA200's 20-bar slope clipped to its negative side.
- Comparison: falling beyond the coin's usual drift -> kept: forward returns are judged against the coin's own average return.
- Outcome: the coin falls further over the following bars, more as the SMA declines faster -> kept: the short is sized by the steepness of the decline, and its gain is measured against that steepness.
- Verdict transfer: yes: the test shorts exactly the stated situation, sized by the stated quantity, and stays flat under a rising average or above it.
Forecast: The detector puts a bar in the "trending" label when the close is below its 200-bar SMA (percent distance below 0); every other bar is flat. In that regime the forecast comes from the 200-bar SMA's percent change over the last 20 bars. It is standardised against its own past 220 values and then clipped at a maximum of 0. A rising average gives 0, so no short is taken. A falling average gives a short that grows in proportion to how fast the average falls, capped at -20. The forecast is never positive.
Config: 002-04_price-cross-below-long-sma.d1_shorts-under-falling-average_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: Take non-overlapping 20-bar cases on each window's grid where the forecast is below 0. For each case, compute allocation x (the coin's 20-bar return minus the coin's mean 20-bar return over all windows), before costs. The measure is the ordinary t of the mean of these values.
- Supporting check: Across the same cases, regress the excess 20-bar return on |forecast|. The slope must be below 0, so that steeper declines are followed by larger falls beyond drift.
- Confirm: The main t is 2 or more and the supporting slope is below 0.
- Reject: The main t is -2 or less, meaning the shorts lose against the coin's drift.
- Inconclusive: A main t between -2 and 2 is inconclusive. So is a main t of 2 or more when the slope is not below 0. So is any result from fewer than 30 active cases.
