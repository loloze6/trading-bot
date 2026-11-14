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
- Situation: short average has just crossed above the long average -> adapted: "after the cross" becomes "while SMA50 is above SMA200", graded by the size of the gap.
- Comparison: versus random points -> adapted: judged against simply holding the coin over the same bars.
- Outcome: price keeps rising, more often and further -> kept: the forward return of the coin while long, upward.
- Verdict transfer: yes: a long position sized by an up-cross state that beats random holding confirms the idea, and one that loses to it rejects the idea.
Forecast: The percent gap between the 50-bar and 200-bar simple moving averages of the close, which is the conventional daily golden-cross pair. The gap is standardised against its own past 200 values. Negative values are clipped to 0, because the idea covers only upward crosses. The forecast is positive while SMA50 is above SMA200 and grows as the gap widens. It is zero while SMA50 is at or below SMA200, so it is never short.
Config: 002-01_sma-upcross-upward-drift_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: The coin's forward 20-bar return after bars with forecast > 0, minus its forward 20-bar return after all bars, before costs. Overlapping returns are counted once by using non-overlapping 20-bar blocks pooled across the 6 windows. The result is reported as a t-statistic.
- Supporting check: The slope of the forward 20-bar return on forecast size, across bars with forecast > 0. It should be positive if wider gaps carry further rises.
- Confirm: Excess forward return while long has t ≥ +2 and the supporting slope is not negative.
- Reject: Excess forward return while long has t ≤ -2, meaning prices after up-crosses fall relative to random points.
- Inconclusive: Any t strictly between -2 and +2 is inconclusive, including an estimate near zero. The test also needs at least 8 non-overlapping 20-bar blocks with forecast > 0 and at least one up-cross across the windows; fewer than that is inconclusive.
