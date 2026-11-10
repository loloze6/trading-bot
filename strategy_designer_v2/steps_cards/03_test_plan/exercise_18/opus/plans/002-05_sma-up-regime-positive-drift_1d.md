---
idea: 002-05_sma-up-regime-positive-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: short SMA above long SMA, from up-cross until down-cross -> adapted: the on/off state "fast above slow" becomes the graded SMA spread, clipped to its positive side.
- Comparison: random stretches of the same length -> kept: bars outside the stretch, and simply holding the coin, serve as the random baseline.
- Outcome: price rises more often and further during the stretch -> kept: next-bar coin returns on in-stretch bars.
- Verdict transfer: yes: the forecast is non-zero exactly over the up-cross-to-down-cross stretch, so excess returns there test the idea directly.
Forecast: The percent spread of the 50-day SMA over the 200-day SMA (the conventional daily cross pair). It is standardised against its own past 200 values and then clipped at 0. The forecast is positive on every bar after an upward cross and before the next downward cross. It grows with how far the short average sits above the long one. It is exactly 0 from a downward cross until the next upward cross. It is never negative.
Config: 002-05_sma-up-regime-positive-drift_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The coin's next-bar return on bars with forecast > 0, minus its next-bar return on bars with forecast = 0. This is a difference of means with a t-statistic, pooled over all 6 windows and judged before costs. Out-of-stretch bars are the baseline that holding the coin would also earn.
- Supporting check: The share of up days on in-stretch bars minus the share on out-of-stretch bars must have the same sign as the main measure.
- Confirm: The in-stretch mean next-bar return exceeds the out-of-stretch mean with t >= 2, and the up-day share is higher in-stretch.
- Reject: The in-stretch mean next-bar return falls short of the out-of-stretch mean with t <= -2, meaning moves after up-crosses reverse.
- Inconclusive: The test is inconclusive if -2 < t < 2, or if the supporting check disagrees in sign with the main measure. It is also inconclusive if fewer than 100 in-stretch bars or fewer than 100 out-of-stretch bars exist across the windows, or if fewer than 2 distinct up-cross stretches occur.
