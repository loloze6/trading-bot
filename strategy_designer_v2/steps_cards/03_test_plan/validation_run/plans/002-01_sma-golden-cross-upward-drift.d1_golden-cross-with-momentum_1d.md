---
idea: 002-01_sma-golden-cross-upward-drift.d1_golden-cross-with-momentum
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: the 50-day SMA of the close is above the 200-day SMA -> kept
- Comparison: the drift is larger the larger the coin's recent-weeks rise, and holds only while that rise is positive -> kept
- Outcome: the coin keeps drifting upward -> kept
- Verdict transfer: yes: a long position sized by the positive recent-weeks rise under a standing golden cross is what the idea says should earn, and is what this test checks.
Forecast: The regime detector computes the spread of the 50-day SMA over the 200-day SMA. While that spread is above 0, the bar is `trending`; otherwise it is `unknown`, which is flat. In `trending`, the forecast is the coin's 20-bar percent rise ("recent weeks", the conventional one-month lookback on daily bars). It is standardised against its own last 60 values, then clipped at 0. So the forecast is zero while the 20-bar return is negative. When the return is positive, the forecast is positive and grows in proportion to the rise, up to the cap of 20. It never goes short.
Config: 002-01_sma-golden-cross-upward-drift.d1_golden-cross-with-momentum_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: The cases are the bars on the non-overlapping 20-bar grid of each window where the forecast is above 0. For each case, take the coin's 20-bar forward return minus the coin's mean 20-bar return over all windows. The measure is the mean of this excess, tested with the t of the mean.
- Supporting check: Among those cases, split at the median forecast. Take the mean excess of the top half minus the mean excess of the bottom half; the check passes if this difference is above 0.
- Confirm: The mean excess is above 0 with t ≥ 2, and the supporting check passes (top half minus bottom half above 0), with at least 30 cases.
- Reject: The mean excess is below 0 with t ≤ -2, with at least 30 cases.
- Inconclusive: Any t strictly between -2 and 2 is inconclusive. So is t ≥ 2 when the top half does not beat the bottom half. So is any result with fewer than 30 active grid cases.
