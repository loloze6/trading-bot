---
idea: 021-04_thin-cloud-downward-breakdown
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: bf6ee48001bb
---
Fidelity:
- Situation: a daily close that crosses down from above the cloud to below it -> adapted: "after the cross" made "while below the cloud within 26 bars of a cross down from above".
- Comparison: thinner cloud at the cross (width relative to price) against a thicker one -> adapted: the cloud's width relative to price is read on each bar of that stretch, graded, instead of only at the cross.
- Outcome: the coin falls over the next 26 days, more after a thin cloud -> kept: short, held 26 bars.
- Verdict transfer: yes: the short is open only after a cross down from above, is sized by cloud thinness, and is judged by the 26-day fall and its link to that thinness.
Forecast: The forecast is active only in the regime where `IchimokuCloudCrossAgeComponent` (9/26/52, displacement 26) is between -26 and -1. That means the close is below the cloud, the cloud was last left from above, and the cross was at most 26 bars ago. On every other bar it is 0 (flat). In that regime the forecast is short and graded by cloud thinness. It uses `IchimokuCloudWidthComponent` in form "proximity", which is 1 / (1 + width in percent of the close). That value is standardised against its own past 78 values, giving about 10 for a usual width, more for a thinner cloud and less for a thicker one, capped at 20. It is then negated. So the forecast runs from about -5 for a thick cloud, through about -10 for a usual one, down to -20 for a very thin one. It is never positive.
Config: 021-04_thin-cloud-downward-breakdown_1d_config.json
Criterion:
- Horizon: 26 bars
- Main measure: The mean unusual move over the cases, in the short direction. A case is a short bet: the forecast falls by at least 2 points on the short side, read once per 26-bar grid cell. The unusual move is the coin's 26-bar return from the signal's close minus its normal 26-bar drift (holding the coin), with the sign flipped. Its t is the ordinary t of the mean over the cases.
- Supporting check: Split the cases at the median |forecast| at entry. Thinner-cloud half minus thicker-cloud half of the unusual move, Welch t.
- Confirm: The mean unusual move is positive with t >= 2 (the coin falls more than its normal drift), and the thin-minus-thick difference is positive with t >= 1.
- Reject: The mean unusual move has t <= -2 (the coin rises more than its drift after the cross), or the thin-minus-thick difference has t <= -2.
- Inconclusive: Any result in between counts as inconclusive. This includes a positive mean with t below 2, and a main confirm whose check t is between -2 and 1. Fewer than 30 cases over all coins and windows is inconclusive whatever the t.
