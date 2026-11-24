---
idea: 031-02_wide-flat-day-ends-downrun
brief: 031_wide-flat-day-ends-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 31f1a8c6c7f6
---
Fidelity:
- Situation: after a 5-day fall, a day with a range wide against its 20-day average range and a close near its open -> adapted: a regime holds only on such days (close below its level 5 days ago, range at least its 20-day mean, body at most 10% of the range by the doji convention); inside it the forecast grows with the range ratio and the flatness.
- Comparison: the day's range against its 20-day average range, and the close against the open -> kept
- Outcome: the price rises over the next 5 days, more for wider and flatter days -> kept: the position is long and is held for 5 bars.
- Verdict transfer: yes: the regime is exactly the idea's situation, the size follows its two strengths, and the outcome is the 5-day rise after it.
Forecast: The forecast is not zero only on days when three things hold. The close is below its level 5 days earlier. The day's high-low range is at least its 20-day mean bar range (FallGatedRangeMultiple with period 1, base 20 and fall 5, at 1.0 or more). The body is at most 10% of the range (BarBodySize flatness, 0.9 or more). On such a day the forecast is long. It is the equal-weight mean of two standardised values (window 60): - the day's range over its 20-day mean bar range (RangeCompressionRatio with short period 1, long period 20, mean_bar_range, width); - the flatness (1 − body/range). It is about +10 at the threshold and rises toward +20 as the day gets wider and flatter. On every other day it is 0.
Config: 031-02_wide-flat-day-ends-downrun_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The unusual move per case. A case is a long bet, that is a rise of the forecast of at least 2 points, read once per 5-bar grid cell. Its unusual move is the coin's 5-day return from the case's close minus the coin's normal 5-day drift (holding the coin, over all windows). The measure is the mean of these moves, with its t computed with the cases of one day taken together.
- Supporting check: none
- Confirm: The mean unusual move is positive with t ≥ 2, over at least 30 cases.
- Reject: The mean unusual move is negative with t ≤ -2, over at least 30 cases.
- Inconclusive: A t between -2 and 2 is inconclusive, and so is any result on fewer than 30 cases.
