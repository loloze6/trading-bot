---
idea: N8-02_near-high-drift-not-overextended
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a new 20-day closing high, then the close stays near that high and above its 20-day average -> adapted: "after the high" becomes "while the high is recent", graded by bars since it, and nearness and distance above the average become graded readings.
- Comparison: the coin's own average rise, and no very large rise over the prior 30 days -> kept: the 30-day run is a regime veto at its top decile, and the average is the coin's mean return over all windows.
- Outcome: the coin rises more than its average over the following days -> adapted: the holding period is dropped, and the position lasts while the situation lasts.
- Verdict transfer: yes: the graded near-high long, flat after an outsized 30-day run, is the idea's own bet, so its gain or loss against holding judges the idea.
Forecast: The forecast is the equal-weight mean of three standardised, long-only readings, each with window 60 and min_periods 20: - BarsSinceHighComponent (lookback 20, max_bars 20): 20 on the day of a new 20-day closing high, one less each bar after, 0 once the high is 20 bars old. - DonchianBreakoutComponent (period 20), clipped at 0: how near the close sits to the top of its 20-day range, 0 in the lower half. - MovingAverageDistanceComponent (SMA 20), clipped at 0: the percent distance above the 20-day average, 0 below it. How it grows and when it is zero: - It is positive and largest just after a fresh high, with the close at the high and well above its average. - It shrinks smoothly as the high ages, the close falls back in its range or nears the average. - It is zero when none of the three is present. It is never negative. - A veto forces the flat regime when the 30-day price change ranks in the top 10 percent of its own history. That is the "very large prior run" exception.
Config: N8-02_near-high-drift-not-overextended_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The slope of the next-10-bar close-to-close return on the forecast, pooled over all coins and windows, before costs. The return is taken minus the coin's mean 10-bar return over all windows together. Its t-statistic uses non-overlapping 10-bar steps, or an equivalent overlap-corrected error.
- Supporting check: The mean excess 10-bar return on bars with forecast > 0 should be above the mean excess on vetoed bars.
- Confirm: The slope is positive with t >= 2.
- Reject: The slope is negative with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. The test also needs at least 30 non-overlapping 10-bar cases with forecast > 0, pooled; with fewer it is inconclusive whatever the t.
