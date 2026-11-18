---
idea: 010-01_rsi-above-midpoint-continues-up
brief: 010_rsi-midline-regime-direction
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 791f9c660ae8
---
Fidelity:
- Situation: share of the past 14 days that the 14-day RSI spent above its midpoint -> kept
- Comparison: a larger share against a smaller one, graded -> kept
- Outcome: the coin's rise over the next 7 days, larger with a larger share -> kept
- Verdict transfer: yes: the forecast is the 14-day RSI-above-50 share, centred at one half, so the test measures the stated relation directly.
Forecast: The forecast is the share of the last 14 daily bars on which the 14-day RSI was above 50, minus one half. It comes from RsiAboveMidlineShareComponent with period 14, window 14, rsi_window 100 and side "above". This is standardised against its own past 60 values (min_periods 20), with no other transform. It is positive (long) when RSI held above 50 on more than 7 of the 14 bars, and it grows in steps of 1/14 up to +0.5 when RSI was above 50 on every bar. It is negative (short) when RSI held above 50 on fewer than 7 bars. It is 0 at exactly 7 of 14. It is ungated and active on every bar, with a cap of ±20.
Config: 010-01_rsi-above-midpoint-continues-up_1d_config.json
Criterion:
- Horizon: 7 bars
- Main measure: On non-overlapping 7-bar samples (positions 0, 7, 14, ... of each window), regress the coin's 7-bar forward return minus that coin's mean 7-bar return (all windows together) on the forecast at the sample bar. Pool all coins and windows and report the slope's t-statistic.
- Supporting check: The book's mean daily timing gain before costs is above 0. Timing gain is the book's mean daily return minus its gain from the market's own rise.
- Confirm: The slope's t is 2 or more, with at least 300 independent cases, and the supporting check passes.
- Reject: The slope's t is -2 or less, with at least 300 independent cases: later moves run against the side RSI held.
- Inconclusive: A t between -2 and 2, or a confirming slope whose timing check fails, neither confirms nor rejects. Fewer than 300 independent cases is also inconclusive. About 1,200 cases are expected: about 17 per window × 24 windows × 3 coins.
