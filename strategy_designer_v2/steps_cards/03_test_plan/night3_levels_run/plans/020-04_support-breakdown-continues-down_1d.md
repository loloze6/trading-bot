---
idea: 020-04_support-breakdown-continues-down
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: d79aab634da6
---
Fidelity:
- Situation: a close below a price where the coin turned up several times in the past 90 days -> adapted: "closes below" becomes "while below", graded by the depth under the level times its touch count.
- Comparison: the more times the level held, the larger the fall -> kept: the swing-low touch count N within 2% multiplies the forecast.
- Outcome: the price keeps falling over the next 5 days -> kept: short, with the bet held 5 bars.
- Verdict transfer: yes: the forecast is short in proportion to breaks of repeatedly held 90-day support, and is judged on the next 5 days' move.
Forecast: The forecast uses one component, TouchWeightedSupportBreakDepthComponent (period 90, side 2, band 2.0). Its raw value is N x the percent depth of the close under a swing-low level of the prior 90 bars. N is that level's count of turn-ups within 2%. The value is 0 when the close is above every swing low. It is standardised over its past 91 values and then negated. The forecast is therefore 0 when no support is broken. Otherwise it is negative, and it grows more negative as the close sits deeper under the level and as the level held more times. It is never positive.
Config: 020-04_support-breakdown-continues-down_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The measure is the unusual move per case. A case is a short bet: the forecast falls by at least 2 points, read once per non-overlapping 5-bar grid cell of each window. The unusual move is the coin's 5-bar return from the signal bar minus the coin's mean 5-bar return over all windows, taken in the short direction. Cases from all coins are pooled, and the measure is the t of their mean.
- Supporting check: The check uses the same cases, split at the median of |forecast| at the signal bar. The mean unusual move of the larger half minus that of the smaller half must be above 0.
- Confirm: The idea is confirmed when the mean unusual move has t >= 2 and the larger-forecast half shows a larger mean move than the smaller half.
- Reject: The idea is rejected when the mean unusual move has t <= -2, meaning that after support breaks the price rises more than usual.
- Inconclusive: A t between -2 and 2 is inconclusive. So is t >= 2 with a failed check, or fewer than 30 cases pooled across coins.
