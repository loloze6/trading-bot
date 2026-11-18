---
idea: 006-04_upside-squeeze-break-continuation
brief: 006_range-compression-precedes-expansion
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 70a362722b07
---
Fidelity:
- Situation: the coin closes above the high of the prior 20-day band -> adapted: the break is an on/off regime rule, and it is held only "while" the close is above that high.
- Comparison: the narrower the 20-day band against the coin's 100-day range -> kept: 1 minus the 20-bar range over the 100-bar range. The 20-bar window includes the break bar itself.
- Outcome: price keeps rising beyond the band's top over the next 3 days -> adapted: the 3-day hold is dropped. It is measured as the 3-bar return from the break bar's close.
- Verdict transfer: yes: the test grades the size of each break-bar position by band narrowness and judges the 3-bar rise that follows, so a confirm or a reject carries over to the idea.
Forecast: Each bar is checked against the high of the 20 bars before it, using DistanceFromHighComponent(period 20, source high, exclude_current 1, form percent). - If the close is above that high, the bar is classed `trending`. On every other bar the forecast is 0. - On `trending` bars the forecast is long. Its size is RangeCompressionRatioComponent(short 20, long 100), standardised over its own past 100 values (min 25). - That ratio runs from 0 to 1 and is always positive, so the forecast is positive and grows as the 20-bar band narrows against the 100-bar range. It is about +10 at an average narrowness and capped at +20.
Config: 006-04_upside-squeeze-break-continuation_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: - Cases: the non-overlapping 3-bar grid points (positions 0, 3, 6, … of each window) where the forecast is above 0, which are the break bars. - Return: each case's 3-bar forward return, minus the coin's mean 3-bar return over all windows (the holding-the-coin baseline). All returns are before costs. - Measure: the OLS slope of that excess return on the forecast, with its t-statistic.
- Supporting check: On the same cases, the mean excess 3-bar return is above 0.
- Confirm: Both of these hold: - the slope's t is 2 or more; - the mean excess 3-bar return on break-bar cases is positive.
- Reject: The slope's t is -2 or less. A narrower band is then followed by a smaller rise beyond the break.
- Inconclusive: - A slope t between -2 and 2 is inconclusive. - A slope t of 2 or more with a mean excess return of 0 or below is also inconclusive. - With fewer than 100 break-bar cases across all coins and windows, the result is inconclusive whatever the t.
