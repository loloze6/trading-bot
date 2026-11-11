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
- Situation: the stretch between an upward SMA cross and the next downward cross -> adapted: "short above long" (on/off) made graded by the spread's size, zero outside the stretch.
- Comparison: random stretches of the same length -> kept: in-stretch bars against all bars of the same coin and window (holding the coin).
- Outcome: price rises more often and further during the stretch -> kept: next-bar returns of in-stretch bars against the rest.
- Verdict transfer: yes: the forecast is positive on exactly the cross-to-cross bars and the measure compares those bars' returns with holding the coin.
Forecast: The spread of the 50-day SMA over the 200-day SMA, in percent of the 200-day SMA. It is standardised against its own past 200 values (target 10, cap 20), then clipped at 0. The forecast is positive only while the 50-day SMA is above the 200-day SMA, which is the stretch from an upward cross to the next downward cross. It grows as the short average pulls further above the long one. It is zero at the cross itself and on every bar after a downward cross. It is never short.
Config: 002-05_sma-up-regime-positive-drift_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Mean next-bar close-to-close return on in-stretch bars (forecast > 0) minus the mean next-bar return on out-of-stretch bars (forecast = 0). Pooled over the 6 windows with a Welch t-stat; each daily return is counted once.
- Supporting check: Share of up next-bars in-stretch minus share out-of-stretch, which tests "more often".
- Confirm: The in-stretch minus out-of-stretch mean next-bar return is positive with t >= 2.
- Reject: The difference is negative with t <= -2, which means moves after up crosses reverse.
- Inconclusive: Any |t| < 2 is inconclusive. The test also needs at least 100 in-stretch bars, 100 out-of-stretch bars and at least 3 distinct up-cross stretches across the windows. With fewer, the result is inconclusive whatever the t.
