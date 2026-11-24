---
idea: 031-04_downrun-size-scales-wide-flat-reversal
brief: 031_wide-flat-day-ends-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 31f1a8c6c7f6
---
Fidelity:
- Situation: a day whose range is wide against its 20-day average daily range and whose close lands near its open -> adapted: a regime that holds only on days where the range is at least 1.5 times the 20-day mean bar range and the body is at most 10% of the range (the doji convention); flat on all other days.
- Comparison: the day's range against its 20-day average daily range -> kept
- Outcome: the larger the fall over the preceding 5 days, the larger the rise over the next 5 days -> adapted: the long position grows with the 5-day fall, measured in usual 5-day moves, and is 0 after a 5-day rise; it is held for 5 bars.
- Verdict transfer: yes: the forecast exists only on wide, flat days and is graded by the prior 5-day fall, so a slope of the next 5-day return on that forecast confirms or rejects the idea directly.
Forecast: On days where the regime detector finds a wide, flat day, the forecast is the coin's 5-day fall. That fall is the negated 5-day close-to-close return, standardised against its own past 60 values, so 10 is a usual 5-day move. It is clipped at 0, so it is long and grows with the size of the fall, and it is 0 when the coin rose. The two conditions are: the day's range is at least 1.5 times the mean daily range of the 20 days ending today, and |close − open| is at most 0.1 of the day's range. On every other day the forecast is 0. The 5-day return includes the signal day, whose close-to-open move is at most 10% of its range, so it adds almost nothing to the prior fall.
Config: 031-04_downrun-size-scales-wide-flat-reversal_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Cases are bars in the mean_reversion regime. For each case, take the coin's 5-bar forward return minus its mean 5-bar return over all windows, and regress it on that bar's forecast. Within a coin and window, a case that falls inside the 5 bars after a kept case is dropped. The slope's t-statistic uses cases summed per day.
- Supporting check: Take the cases with forecast ≥ 2. Their mean 5-bar return in excess of holding the coin must be above 0.
- Confirm: The slope is positive with t ≥ 2 and the supporting check passes.
- Reject: The slope is negative with t ≤ −2.
- Inconclusive: Any other result is inconclusive, including a slope with |t| < 2 or a positive slope whose check fails. At least 30 independent cases are needed, with at least 10 having forecast ≥ 2; fewer cases is inconclusive.
