---
idea: 045-01_agitated-wide-low-close-rebound
brief: 045_agitated-wide-day-close-location-fade
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 0e977cd77240
---
Fidelity:
- Situation: in an agitated market, the day closes low in its high-low range on a wide day -> kept: the close's distance under the day's high, counted in the prior 30 days' mean daily range; the agitated profile is added by code.
- Comparison: the day's range against its usual daily range over the past 30 days -> kept: the mean high-low range of the 30 prior days.
- Outcome: the coin rises more over the next day, the lower and wider the close -> kept: the next 1-day return, graded by position size.
- Verdict transfer: yes: the forecast is the idea's own product of close location and range width, held one day.
Forecast: One component, `BreakoutInMeanRangesComponent` with period 1, base_period 30, side "below", high_current 1 and base_exclude_current 1. Its raw value is (high − close) divided by the mean high-low range of the 30 prior days. That equals (high − close)/(high − low) times the day's range over its usual range, so it is the idea's product. It is standardised over its past 60 values, with min_periods 20. The forecast is never negative and is long only. It is 0 when the day closes at its high. It grows as the close sits lower in the range and as the range widens against its usual size, averaging about +10 and capped at +20. Outside the agitated profile, code keeps the book flat.
Config: 045-01_agitated-wide-low-close-rebound_1d_config.json
Profile: agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: A pooled least-squares slope over all coins and windows, on bars with a nonzero forecast. Each case's next-day return, minus that coin's mean daily return over all windows, is regressed on the bar's forecast (`post_pipeline_value`). The slope's t has cases of the same day summed together.
- Supporting check: none
- Confirm: The slope is positive with t ≥ 2, on at least 300 cases spread over at least 150 distinct days.
- Reject: The slope is negative with t ≤ −2, on the same minimum of cases and days.
- Inconclusive: Any t between −2 and 2 is inconclusive, and so is a result on fewer than 300 cases or fewer than 150 distinct days.
