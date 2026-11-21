---
idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: d79aab634da6
---
Fidelity:
- Situation: daily close just below prices where the coin turned up several times in the past 90 days -> adapted: "just below" and "several" made graded, as the number of 90-day swing lows near the nearest one above the close, times the close's nearness to it.
- Comparison: the more such turning-up lows lie just above the close, the larger the fall -> kept: the forecast grows with that count.
- Outcome: the price falls over the next 5 days -> kept: short, held for 5 daily bars.
- Verdict transfer: yes: the forecast is short exactly when, and as much as, the close sits just under a support that held many times, and it is judged on the 5-day move after it.
Forecast: One component, `SwingHighClusterCountComponent` set to swing lows (`pivot` "low", `level` "above"), with `period` 90, `side` 2, `band` 2.0 and `form` "proximity" with `power` 1. It finds the lowest 90-day swing low at or above the close. It counts the swing lows within 2 % of that level, and multiplies the count by 1/(1 + D), where D is the close's percent distance below the level. The result is standardised against its last 90 values and negated. The forecast is therefore zero or negative: zero when no swing low lies above the close. It grows in size with the number of past turning-up lows clustered at the level and with how close the close sits under it. It never goes long.
Config: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are the bets, each read once per 5-bar grid cell of each window. A bet is a fall of the forecast on the short side of at least 2 points. For each case, take the coin's 5-bar return from the signal bar's close, minus the coin's normal 5-bar drift over all windows, in the short direction. Take the mean of this unusual move over all cases and coins, with its t of the mean.
- Supporting check: Split the cases at the median of |forecast| on the signal bar. The mean unusual move of the larger half minus that of the smaller half must be above 0.
- Confirm: The mean unusual move in the short direction is positive with t >= 2 over at least 30 independent cases, and the supporting check passes.
- Reject: The mean unusual move in the short direction is negative with t <= -2 over at least 30 independent cases, meaning the price rises more than its normal drift after the signal.
- Inconclusive: Any t between -2 and 2, a confirming t with a failed supporting check, or fewer than 30 independent cases.
