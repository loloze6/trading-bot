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
- Situation: short SMA above long SMA, from up-cross to down-cross -> adapted: "after the cross until the opposite cross" becomes "while the 50 SMA is above the 200 SMA", sized by the spread.
- Comparison: random stretches of the same length -> adapted: daily returns on up-stretch bars against daily returns on all bars (holding the coin).
- Outcome: price rises more often and further during the stretch -> kept
- Verdict transfer: yes: the forecast is long exactly on the up-stretch bars, so their excess return over all bars confirms or rejects the idea.
Forecast: The forecast is the 50-day SMA minus the 200-day SMA, as a percent of the 200-day SMA, standardised against its own past 200 values. It is clipped at 0, so it is long only. It is positive only while the short average is above the long one, which is the stretch between an upward cross and the next downward cross. It grows as the gap between the averages widens, up to the cap of 20. It is zero whenever the short average is at or below the long one.
Config: 002-05_sma-up-regime-positive-drift_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Take the coin's next-bar close-to-close return on bars where the forecast is above 0. Compare its mean with the mean next-bar return over all tested bars (holding the coin). Use non-overlapping 1-bar returns pooled across the 6 windows, with a t-statistic on the difference.
- Supporting check: The share of up days on bars with a positive forecast, against the share of up days over all bars.
- Confirm: The mean next-bar return on positive-forecast bars exceeds the all-bars mean with t ≥ 2, and the up-day share on those bars is higher than over all bars.
- Reject: The mean next-bar return on positive-forecast bars is below the all-bars mean with t ≤ -2, meaning up-stretches underperform holding.
- Inconclusive: Any t between -2 and 2 is inconclusive, as are cases where the main measure and the up-day share disagree in sign. The test also needs at least 150 bars with a positive forecast and at least 100 bars at zero across the windows; with fewer, the result is inconclusive.
