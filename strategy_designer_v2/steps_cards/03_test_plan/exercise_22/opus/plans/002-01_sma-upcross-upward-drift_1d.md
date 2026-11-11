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
- Situation: short average has just crossed above the long average -> adapted: "after the cross" made "while the 50-day SMA is above the 200-day SMA", graded by the size of the gap.
- Comparison: random points in time -> kept: future returns are judged against the coin's average return over the same window (simply holding it).
- Outcome: price keeps rising, more often and further -> kept: forward returns of the coin, long side only.
- Verdict transfer: yes: a long position that grows with the bullish SMA gap is the idea's persistence claim in the only form the config allows, so a confirm or reject carries over.
Forecast: The forecast uses one indicator, the SMA(50) minus SMA(200) spread on daily closes, as a percent of SMA(200). It is standardised against its own past 200 values, with target 10 and cap 20. It is then clipped at 0, so it is long-only. The forecast is positive and grows with the gap while the 50-day average is above the 200-day average. It is zero while the 50-day average is below. It is never negative.
Config: 002-01_sma-upcross-upward-drift_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The slope of a regression of each sample's 10-bar forward excess log return on the forecast at the sample bar. The excess return is the coin's 10-bar forward log return minus that window's average 10-bar log return. Samples are taken every 10th bar, so overlapping returns are counted once. All 6 windows are pooled, and returns are before costs.
- Supporting check: The mean 10-bar forward excess return on samples with forecast > 0, compared with samples where the forecast is 0. This uses the same non-overlapping samples and a Welch t-test.
- Confirm: A slope with t ≥ 2, together with a supporting difference that is positive.
- Reject: A slope with t ≤ -2, meaning that larger bullish gaps are followed by below-average returns (reversal).
- Inconclusive: A slope with |t| < 2, including results near zero. A test with fewer than 60 non-overlapping samples in total, or fewer than 25 with forecast > 0, is also inconclusive.
