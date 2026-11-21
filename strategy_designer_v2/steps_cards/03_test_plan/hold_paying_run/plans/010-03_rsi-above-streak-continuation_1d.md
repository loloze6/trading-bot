---
idea: 010-03_rsi-above-streak-continuation
brief: 010_rsi-midline-regime-direction
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 70a362722b07
---
Fidelity:
- Situation: the 14-day RSI has stayed above 50 without a break, counted in days up to the current close -> kept: `RsiMidlineAgeComponent` (period 14) counts the current run above 50, and the clip at 0 drops the below-50 side.
- Comparison: a longer stretch gives a higher return than a shorter one -> kept: the position grows with the run length, and the gain is judged against the size of the position.
- Outcome: the coin's return over the next 14 days is higher -> kept: the horizon is 14 bars on daily bars.
- Verdict transfer: yes: the test measures exactly the stated run length against the 14-day return, so its result transfers to the idea in both directions.
Forecast: One indicator, `RsiMidlineAgeComponent` (RSI period 14, cap 60 bars, RSI window 100, all at convention). Its raw value is +n while RSI(14) has been above 50 for the last n days, and negative while RSI is below 50. It is standardised over its past 160 values (min_periods 40), then clipped at 0. The forecast is long only. It is zero while RSI is at or below 50, and starts small on the first day above 50. It then grows with each further unbroken day above 50, up to the 60-day cap and the standardise cap of 20. It drops back to zero on the day RSI falls back to 50 or below.
Config: 010-03_rsi-above-streak-continuation_1d_config.json
Criterion:
- Horizon: 14 bars
- Main measure: On a non-overlapping 14-bar grid in each window, pooled over the three coins, regress the coin's excess 14-bar forward return on the bar's forecast. The excess return is close[t+14]/close[t]-1 minus that coin's mean 14-bar return over all windows. The measure is the slope's t-statistic, with the number of cases given next to it.
- Supporting check: The timing part of the book's mean daily return, before costs, is above 0. The timing part is the book's mean daily return minus the part due to the market's own rise.
- Confirm: The slope's t is 2 or more, and the supporting check passes.
- Reject: The slope's t is -2 or less: longer stretches above 50 are followed by lower excess 14-day returns.
- Inconclusive: Any t between -2 and 2, or a t of 2 or more with the check failing, is inconclusive. Any result with fewer than 300 grid cases in total, or fewer than 100 cases with a forecast above 0, is also inconclusive.
