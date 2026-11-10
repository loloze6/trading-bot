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
- Situation: short average has just crossed above the long average -> adapted: "after the cross" made "while SMA50 is above SMA200", graded by the size of the spread.
- Comparison: price after random points -> kept: forward returns are judged against all bars, which is the same as holding the coin.
- Outcome: price keeps rising, more often and further -> kept: forward close-to-close return over a fixed horizon, upward.
- Verdict transfer: yes: a long position that grows with the up-spread profits beyond holding only if rises persist after up-crosses, and fails if they do not persist or if they reverse.
Forecast: The forecast uses the 50-day SMA minus the 200-day SMA, divided by the SMA200, in percent (EMASpreadComponent with average "sma"). It is standardised against its own past 200 values, so a typical spread gives about +10, capped at +20. It is then clipped at 0 because the idea is only about upward crosses. The forecast is positive while SMA50 is above SMA200 and grows as the short average pulls further above the long one. It is zero while SMA50 is at or below SMA200, and it is never negative.
Config: 002-01_sma-upcross-upward-drift_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Regress the forward 10-bar close-to-close return, minus that window's mean 10-bar return (the holding drift), on the forecast. Use non-overlapping 10-bar samples pooled across the 6 windows, before costs.
- Supporting check: Compare the share of positive forward 10-bar excess returns on bars with forecast > 0 against the share on bars with forecast = 0, using the same non-overlapping samples.
- Confirm: The slope is positive with t ≥ 2.
- Reject: The slope is negative with t ≤ -2, meaning moves after up-crosses reverse.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a test with fewer than 40 non-overlapping samples in total, or fewer than 15 samples with forecast > 0.
