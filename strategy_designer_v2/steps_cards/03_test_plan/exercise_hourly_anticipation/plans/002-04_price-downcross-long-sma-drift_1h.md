---
idea: 002-04_price-downcross-long-sma-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: close below the long average after being above it -> adapted: "after the down-cross" becomes "while below", graded by the percent distance under the SMA200.
- Comparison: random points -> kept: active bars are judged against all bars of the same window, which is the same as simply holding the coin.
- Outcome: price keeps falling, more often and further -> kept: measured as the forward return over the horizon, short side only.
- Verdict transfer: yes: a short that grows with depth below the long average gains before costs only if price keeps falling after it moves below that average.
Forecast: The forecast is the percent distance of the close from its 200-bar simple moving average, where the average includes the current close. It is standardised against its own past 200 values and clipped at a maximum of 0, so it is short-only. It is zero while the close is at or above the SMA200. It turns negative as soon as the close drops below the average and grows smoothly more negative the further below it sits, down to the cap of -20.
Config: 002-04_price-downcross-long-sma-drift_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: For each bar where the forecast is below 0, take the coin's 24-bar forward return. Subtract the mean 24-bar forward return over all bars of the same window. Sample non-overlapping 24-bar blocks only, and pool the 6 windows.
- Supporting check: Compare the share of active blocks with a negative 24-bar forward return against that share over all blocks of the same window.
- Confirm: The mean excess forward return on active blocks is below 0 with t ≤ -2. The same sign must hold in at least 4 of the 6 windows. The negative-return share on active blocks must exceed the all-bar share.
- Reject: The mean excess forward return on active blocks is at or above 0, meaning no extra fall or a reversal. Also reject if it is negative with t > -1 and the sign agrees in 3 or fewer windows.
- Inconclusive: t between -2 and -1, or windows split 3 to 3. A verdict requires at least 100 pooled non-overlapping active blocks and at least 10 in each window; with fewer, the result is inconclusive.
