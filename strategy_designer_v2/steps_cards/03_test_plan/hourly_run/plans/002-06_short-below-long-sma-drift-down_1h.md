---
idea: 002-06_short-below-long-sma-drift-down
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: short SMA below long SMA on hourly bars -> adapted: the on/off zone made graded by how far the short SMA sits below the long one, and zero outside the zone.
- Comparison: price moves at random points -> kept: in-zone forward returns are judged against the coin's unconditional forward return over the same window.
- Outcome: price falls over the next bars, more often and further -> kept: measured as forward 24-bar coin returns after zone bars, by sign and by size.
- Verdict transfer: yes: the graded short position is held exactly while the short SMA is below the long SMA, so its excess gains confirm or reject the zone's downward drift.
Forecast: The forecast uses the SMA50 minus SMA200 spread on 1h closes, as a percent of SMA200. The 50/200 pair is the conventional choice because the brief gives no periods. The spread is standardised against its own past 200 values, then clipped at a maximum of 0. When the short SMA is above the long one, the forecast is 0 (flat). When the short SMA is below, the forecast is negative (short). The short grows with the depth of the spread, up to -20. Near the cross the spread is about 0, so the position builds smoothly and never jumps.
Config: 002-06_short-below-long-sma-drift-down_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: Take non-overlapping 24-bar blocks, pooled over the 6 windows. Regress the coin's next-24-bar return, minus that window's mean 24-bar return (the buy-and-hold drift), on the forecast at the block's start. The measure is the slope's t-stat. A positive slope means deeper shorts precede larger excess falls.
- Supporting check: Among blocks starting in the zone (forecast < 0), the share whose excess 24-bar return is below 0. Compare it with 50% using a binomial test.
- Confirm: Slope t >= 2, with an in-zone share of falling blocks above 50%.
- Reject: Slope t <= -2, meaning in-zone blocks are followed by excess rises (reversal).
- Inconclusive: Slope t between -2 and 2, or fewer than 60 in-zone non-overlapping blocks across the 6 windows. The 60-block minimum applies in every case.
