---
idea: 047-04_falling-agitated-range-scaled-fade
brief: 047_agitated-downtrend-scaled-days-reverse
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: bd33e939b067
---
Fidelity:
- Situation: an up day in a falling, agitated market, sized by its rise in units of the 30-day average daily range -> kept: BreakoutInMeanRangesComponent gives the close-to-close rise over the 30-day mean bar range; it is 0 on every non-up day, and the code adds the profile.
- Comparison: none in the idea; the brief compares against ordinary days in the profile -> kept: the criterion compares cases with all profile bars.
- Outcome: the price falls over the next 3 days, more after a larger rise -> kept: the forecast is short, graded by the rise, and each bet is held 3 bars.
- Verdict transfer: yes: the book shorts exactly the profile's up days, sized by the idea's own scaled rise, over the idea's 3-day horizon.
Forecast: A single component measures the day's close-to-close rise divided by the mean daily range (high minus low) of the last 30 bars, with bar t included. Its settings are BreakoutInMeanRangesComponent with period 1, side "above", source "close", high_current 0, base_period 30 and base_exclude_current 0. It reads 0 on down and flat days and grows linearly with the rise. It is standardised against its own last 60 values and then negated. The forecast is therefore 0 on every non-up day and negative (short) on up days, and the short grows with the scaled rise up to the cap of -20. It is never positive. The profile code keeps the forecast at 0 outside falling agitated bars.
Config: 047-04_falling-agitated-range-scaled-fade_1d_config.json
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: The cases are the bars where the forecast falls by at least 2 points on the short side (a new bet), read once per non-overlapping 3-bar grid cell of each window. For each case, take the coin's 3-day return from the case's close, minus that coin's mean 3-day return over all its falling-agitated grid bars (the bars in the recorded profile regime), with the sign set so that a fall counts as positive. The measure is the mean of these values. Its t is computed with the cases of one day pooled, and it is judged before costs.
- Supporting check: Split the cases at the median of |forecast|. The mean unusual move of the upper half minus that of the lower half must be above 0.
- Confirm: The idea is confirmed when the main measure is above 0 with t ≥ 2, over at least 30 case-days, and the supporting check passes.
- Reject: The idea is rejected when the main measure is below 0 with t ≤ -2, over at least 30 case-days.
- Inconclusive: Any t between -2 and 2 is inconclusive. A confirming t with a failing supporting check is also inconclusive. Fewer than 30 independent case-days is inconclusive whatever the result.
