---
idea: 031-03_uprun-size-scales-wide-flat-reversal
brief: 031_wide-flat-day-ends-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 31f1a8c6c7f6
---
Fidelity:
- Situation: a day whose range is wide against its 20-day average daily range, and whose close lands near its open -> adapted: kept as a regime condition. Today's range must be at least 1.5 times the 20-day mean bar range, and the body must be at most 10% of the day's range (common conventions, since the brief gives no numbers).
- Comparison: the larger the rise over the preceding 5 days, the larger the fall -> kept: the position size is graded by the 5-day rise up to the flat day's close (that day's own body is near flat), and it is zero after a 5-day fall.
- Outcome: the coin falls over the next 5 days -> kept: a short position held for 5 daily bars.
- Verdict transfer: yes: only wide flat days after a rise carry a position, it is sized by the rise, and it is judged on the 5-day fall.
Forecast: The forecast is zero on every day except a wide, flat day. That is a day whose high-low range is at least 1.5 times the mean daily range of the last 20 days (today included) and whose open-to-close body is at most 10% of its range. On such a day the forecast is minus the 5-day percent rise (close[t]/close[t-5]-1), standardised against its own past 60 values (average size about 10, capped at 20) and clipped at 0. It is short and grows with the size of the prior run-up. It is zero if the 5 days fell. It is zero again on the next ordinary day, while the holding period keeps each short for 5 days.
Config: 031-03_uprun-size-scales-wide-flat-reversal_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: A case is a bet: the forecast falls to at least 2 points below zero, read once per 5-bar grid cell. For each case, take the coin's 5-day return after the signal bar's close, minus the coin's normal 5-day drift over all windows, taken in the short direction. The measure is the mean of this unusual move, with its t computed with cases on the same day taken together.
- Supporting check: Split the cases at the median of |forecast|. The above-median cases must have a larger mean unusual move than the below-median cases (difference above 0).
- Confirm: The mean unusual move in the short direction is positive with t ≥ 2, and the supporting check passes.
- Reject: The mean unusual move in the short direction has t ≤ -2, meaning the coin keeps rising after wide flat days that follow a rise.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is t ≥ 2 with a failed supporting check. The test needs at least 30 cases, on at least 30 distinct days, or it is inconclusive.
