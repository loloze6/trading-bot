---
idea: 002-01_sma-upcross-upward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: short SMA has crossed above long SMA -> adapted: "after the cross" made "while short SMA is above long SMA", graded by the size of the spread.
- Comparison: price after random points -> kept: next returns are compared against all bars, which is simply holding the coin.
- Outcome: price keeps rising, more often and further -> kept: next 10-bar forward return of the coin, upward.
- Verdict transfer: yes: the "while above, sized by the spread" form is the allowed adaptation of "after X", and it rises or fails with the same persistence claim.
Forecast: The forecast uses the SMA50/SMA200 spread on daily bars, (SMA50 − SMA200) / SMA200, from EMASpreadComponent with `average` "sma". It is standardised against its own past 200 values and clipped at 0. It is positive and grows with the gap while the 50-day average is above the 200-day average. It is zero while the 50-day average is below. It is never short, because the idea concerns upward crosses only.
Config: 002-01_sma-upcross-upward-drift_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The slope of the coin's next 10-bar return (minus its mean over all tested bars) on the forecast at the start of each step. It uses non-overlapping 10-bar steps pooled across the 6 windows, before costs.
- Supporting check: The mean next 10-bar return on bars with forecast > 0, minus the mean on bars with forecast = 0, using the same non-overlapping steps.
- Confirm: The slope is positive with t ≥ 2, and the supporting difference is positive.
- Reject: The slope is negative with t ≤ −2. This means that after up-crosses, price does worse than at random points.
- Inconclusive: Any t between −2 and 2 is inconclusive. The result is also inconclusive if there are fewer than 20 non-overlapping steps with forecast > 0 or fewer than 20 with forecast = 0.
