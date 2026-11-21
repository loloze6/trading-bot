---
idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c2_broken-support-in-downtrend
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: e48527ec0eac
---
Fidelity:
- Situation: daily close just below several past-90-day turning-up lows -> adapted: a graded count of swing lows near the nearest level above the close, weighted by how close the close sits under it.
- Comparison: only while the 60-day return is negative -> kept: a regime rule on the 60-day return being below 0.
- Outcome: falls over the next 10 days, more with more lows -> kept: a short held 10 bars, sized by the cluster reading.
- Verdict transfer: yes: the forecast is the idea's cluster-under-close reading, active only after a 60-day decline, and is short over the idea's 10-day horizon.
Forecast: The detector puts a bar in `mean_reversion` when the 60-bar price change is below 0. Every other bar is `unknown` and flat. In `mean_reversion`, `SwingHighClusterCountComponent` reads turning-up lows: pivot "low", level "above", 90-bar window, side 2, band 2 percent, form "proximity", power 1. Its value is N x 1/(1+D). N is the number of swing lows within 2 percent of the nearest swing low at or above the close. D is the close's percent distance below that level. The value is standardised over 90 bars (min_periods 22) and then negated. The forecast is 0 when no swing low lies above the close. Otherwise it is negative, and the short grows with the size of the cluster and with how near the close sits under it. It is never positive.
Config: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c2_broken-support-in-downtrend_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Cases are the bars on each window's non-overlapping 10-bar grid where the forecast is below 0. For each case, take the coin's 10-bar return minus its normal drift and multiply it by -1, which puts it in the short's direction. The main measure is the mean of these values weighted by |forecast|, with its t computed over the cases.
- Supporting check: Among the cases, the half with the larger |forecast| shows a larger mean short-direction excess return than the smaller half (difference larger minus smaller > 0).
- Confirm: The weighted mean is above 0 with t >= 2, and the supporting check passes (difference > 0).
- Reject: The weighted mean is below 0 with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A main measure with t >= 2 whose supporting check fails is also inconclusive. So is any result from fewer than 30 cases across all coins and windows.
