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
- Situation: the short moving average has just crossed above the long one -> adapted: "after the cross" becomes "while the short SMA is above the long SMA", graded by the size of the gap.
- Comparison: compared with random points -> kept: judged against all bars, which is the same as simply holding the coin.
- Outcome: price keeps rising over the following bars, more often and further -> adapted: the holding period is dropped; the long position stays while the gap is positive.
- Verdict transfer: yes: the only changes are the allowed ones ("after" made "while", on/off made graded, holding dropped), so a rise after up-crosses shows or fails in the same bars.
Forecast: The forecast is the percent gap between the 50-day and 200-day simple moving averages of BTC. - It is put on the scale of its own past 200 values, so a typical gap gives about +10. - Negative values are clipped to 0, because the idea is only about the upward cross. - The forecast is positive while the 50-day SMA is above the 200-day SMA, and grows as the gap widens. - It is zero while the 50-day SMA is below the 200-day SMA.
Config: 002-01_sma-upcross-upward-drift_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Take the forward 10-bar BTC return on bars with forecast above 0, weighted by the forecast. Subtract the mean forward 10-bar BTC return over all bars in the same windows. Test the difference with a t-statistic computed on non-overlapping 10-bar blocks.
- Supporting check: Compare the share of positive forward 10-bar returns on bars with forecast above 0 with that share on all bars.
- Confirm: The forecast-weighted excess forward return is positive with t >= 2. This holds before costs and across the pooled 6 windows.
- Reject: The forecast-weighted excess forward return is negative with t <= -2. That means moves after up-crosses underperform holding, or reverse.
- Inconclusive: Any t between -2 and 2, including results near zero. Fewer than 20 non-overlapping 10-bar blocks with forecast above 0 is also inconclusive, whatever the t.
