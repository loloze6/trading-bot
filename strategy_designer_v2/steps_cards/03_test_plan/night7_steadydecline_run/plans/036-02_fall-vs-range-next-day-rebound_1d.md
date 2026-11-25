---
idea: 036-02_fall-vs-range-next-day-rebound
brief: 036_outsized-daily-fall-rebounds
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 8ae04f0765bb
---
Fidelity:
- Situation: a one-day close-to-close fall larger than the coin's average daily range -> kept: a regime that holds a position only while the fall is at least one mean range, with the forecast graded by the fall's size inside it.
- Comparison: the average daily high-to-low range over the past 30 days -> kept: the mean of high minus low over the 30 days before the falling day.
- Outcome: the coin rises over the next day, more after a larger fall -> kept: the next 1-bar return, long only.
- Verdict transfer: yes: the config holds a long only on days whose fall exceeds the 30-day mean range, sized by that fall, for one day.
Forecast: The forecast uses `BreakoutInMeanRangesComponent` with `period` 1, `base_period` 30, `side` "below", `high_current` 0, `base_exclude_current` 1 and `source` "close". It reads the day's close-to-close fall, max(0, close[t-1] − close[t]), divided by the mean daily high-low range of the prior 30 days. The regime detector selects `mean_reversion` only when this ratio is at least 1, meaning the fall exceeds the usual daily range. On every other bar the forecast is 0. Inside the regime the forecast is the same ratio standardised (window 60, min_periods 20), so it is always positive (long only) and grows with the fall's size against the range. Because the ratio is 0 on up days, its past mean is small, so most case bars reach the cap of +20. For that reason the graded relation is checked on the raw ratio.
Config: 036-02_fall-vs-range-next-day-rebound_1d_config.json
Side: long only (the brief): each component's forecast capped at 0 by step 3's code
Criterion:
- Horizon: 1 bar
- Main measure: Over the case bars (regime `mean_reversion`, forecast > 0), the next-day return close[t+1]/close[t] − 1 minus the coin's mean daily return over all windows, as a mean with its t. Cases on the same day are summed into one.
- Supporting check: Across the cases, the Spearman correlation between the raw ratio (`fall.last_history_value`) and the next-day excess return is above 0.
- Confirm: The mean next-day excess return is positive with t ≥ 2 and the Spearman correlation is above 0.
- Reject: The mean next-day excess return has t ≤ −2, meaning the largest relative falls are followed by further decline against the coin's drift.
- Inconclusive: Any t between −2 and 2, or t ≥ 2 with a correlation at or below 0. At least 100 case days are required across all coins and windows; with fewer the result is inconclusive.
