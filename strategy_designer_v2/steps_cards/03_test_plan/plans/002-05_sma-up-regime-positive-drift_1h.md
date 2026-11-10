---
idea: 002-05_sma-up-regime-positive-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: stretch from an up-cross of short SMA over long SMA to the next down-cross -> adapted: "after the cross until the opposite cross" becomes "while SMA50 is above SMA200", sized by the spread.
- Comparison: random stretches of the same length -> kept: in-state returns are compared with the coin's return over all bars of the same window.
- Outcome: price rises more often and further during the stretch -> kept: the 24-bar forward return over in-state bars, against holding the coin.
- Verdict transfer: yes: the long position is held on exactly the bars of each up-cross stretch, so its excess return over holding the coin is the idea's claim.
Forecast: The forecast is the SMA50 minus SMA200 spread on 1h closes, in percent of SMA200, from EMASpreadComponent with average "sma". It is standardised over its own last 200 values and clipped at 0, so it is long-only. It is positive only while SMA50 is above SMA200, which is the stretch from an up-cross to the next down-cross. Its size grows with the gap between the averages, up to the cap of 20. It is zero while SMA50 is below SMA200. The 50/200 SMA pair is the usual cross convention; the brief gives no periods.
Config: 002-05_sma-up-regime-positive-drift_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: Use non-overlapping 24-bar blocks that start on bars where the forecast is above 0. Take the mean close-to-close return of these blocks, minus the mean return of all non-overlapping 24-bar blocks in the same window (holding the coin). Judge before costs, pooled over the 6 windows.
- Supporting check: The share of in-state blocks with a positive return, minus the share for all blocks. Within the state, a second reading is whether the block return grows with the forecast's size.
- Confirm: The pooled excess mean return is above 0 with t ≥ 2. The excess is also positive in at least 4 of the 6 windows, and the supporting hit-rate excess is above 0.
- Reject: Either the pooled excess mean return is ≤ 0, or it is negative in at least 4 of the 6 windows. Negative excess means moves after up-crosses reverse.
- Inconclusive: A positive pooled excess with t below 2, or mixed signs across windows (3 of 6). A result also counts as inconclusive if there are fewer than 150 in-state non-overlapping blocks in total, or fewer than 10 distinct up-cross stretches across the windows.
