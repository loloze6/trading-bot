---
idea: 031-01_wide-flat-day-ends-up-run
brief: 031_wide-flat-day-ends-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 051b3422f169
---
Fidelity:
- Situation: after a 5-day rise, a day closing near its open with an unusually wide range -> adapted: the three conditions become a regime (5-day return > 0, body ≤ 10% of range, range ≥ 1.5x the 30-day mean range); "after" becomes "while" on that day.
- Comparison: the day's high-low range against its 30-day average range -> kept
- Outcome: a fall over the next 5 days, larger the wider the range -> kept: a graded short held 5 bars.
- Verdict transfer: yes: the test bets short only on such days, sizes the bet by the day's range multiple, and judges the 5-day move against the coin's drift.
Forecast: The forecast is zero on every bar except one regime. That regime holds when all three of these are true: - the 5-day return is above 0; - the day's body |close − open| is at most 10% of its high-low range; - the day's range is at least 1.5 times the mean daily range of the last 30 days (that day included). On those bars the forecast is short. It is the negation of RiseTimesRangeMultipleComponent (rise_period 5, range_period 30): the 5-day rise in percent times the day's range over its 30-day mean range. That value is standardised over its last 60 values (min 20) and then negated. The short grows with the range multiple and with the size of the run. The forecast is never positive.
Config: 031-01_wide-flat-day-ends-up-run_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: For each case (a short bet on a grid cell of 5 bars), take the coin's 5-day return from the signal bar's close. Subtract the coin's normal 5-day drift over all windows and flip the sign to the short side: this is the unusual move. Take its mean and its day-clustered t, before costs.
- Supporting check: The mean unusual move of cases whose |forecast| is above the median exceeds that of the cases below it (difference > 0).
- Confirm: The mean unusual move is > 0 with t ≥ 2, and the supporting check passes.
- Reject: The mean unusual move is < 0 with t ≤ -2, meaning the coin rises more than its drift after such days.
- Inconclusive: Any t between -2 and 2, or a confirming t with the supporting check failing. Fewer than 30 cases is inconclusive whatever the t.
