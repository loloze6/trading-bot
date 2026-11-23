---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound.d2_wide-falls-rebound-in-uptrends
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 69ac1b38a672
---
Fidelity:
- Situation: a day the coin closes lower, with its high-low range above its 30-day average range -> adapted: the "exceeds" threshold is made graded as the range's multiple of its 30-day mean, on down days only.
- Comparison: stronger while the coin's 30-day return is positive -> adapted: a regime on the sign of the 30-day return, with full size when it is positive and half size otherwise.
- Outcome: the coin's return over the next 3 days is above its usual drift (long) -> kept.
- Verdict transfer: yes: the forecast follows the wide down-day range directly, strengthened in 30-day uptrends, and the outcome is the 3-day return above drift.
Forecast: On each daily close, the component is FallGatedRangeMultipleComponent with period 1, base_period 30, fall_period 1 and lag 0. If the day closed below the prior close, it reads that day's high-low range divided by the mean range of the last 30 days. Otherwise it reads 0. It is standardised over its own past 60 values, so a typical wide down day reads about 10 or more, capped at 20. The forecast is 0 on up days and never negative. It grows with how wide the falling day was against the usual range. When the 30-day return is positive (regime "trending"), the forecast is that value at target 10. Otherwise (regime "unknown"), it is the same value at target 5 with a cap of 10, which is half size.
Config: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound.d2_wide-falls-rebound-in-uptrends_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: Take each window's non-overlapping 3-bar grid and keep the grid bars with forecast > 0. On each, compute the coin's 3-day return minus its normal 3-day drift (all windows together). Regress this excess return on the forecast, pooled over coins and windows. Report the slope's t and the case count.
- Supporting check: On the same cases, compare the mean excess return per unit of forecast in regime "trending" with that in regime "unknown". The check passes if trending minus unknown is above 0.
- Confirm: The slope is positive with t >= 2 on at least 100 cases, and the supporting check passes.
- Reject: The slope is negative with t <= -2 on at least 100 cases.
- Inconclusive: Any slope with t between -2 and 2, a confirming slope whose supporting check fails, or fewer than 100 cases.
