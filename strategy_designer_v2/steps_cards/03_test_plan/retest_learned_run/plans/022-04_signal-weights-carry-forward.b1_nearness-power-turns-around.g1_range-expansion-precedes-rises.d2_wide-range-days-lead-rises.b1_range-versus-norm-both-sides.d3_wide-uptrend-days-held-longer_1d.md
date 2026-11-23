---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d3_wide-uptrend-days-held-longer
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 69ac1b38a672
---
Fidelity:
- Situation: a coin's daily high-low range exceeds its 30-day average range, while its 30-day return is positive -> adapted: the excess is graded (larger excess, larger long), and the uptrend is a regime rule.
- Comparison: the day's range against its average range over the past 30 days -> kept.
- Outcome: the coin's return over the next 6 days is higher than its usual drift (long) -> kept: the book holds each bet 6 bars.
- Verdict transfer: yes: the forecast is the idea's range excess, active only in its uptrend, judged on the 6-day return above drift.
Forecast: The regime is trending when the 30-day close return is above 0 and the day's range is at or above its 30-day mean bar range. On all other bars the forecast is flat. In the trending regime, one component is the ratio of the day's high-low range to the mean bar range of the last 30 days (the day included). It is standardised over 60 bars, so its value is about 10 x ratio / its usual ratio, capped at 20. A constant of -10 is averaged with it at equal weight. The forecast is therefore (x - 10) / 2. It is near 0 for a day of average width and grows smoothly as the day gets wider, up to +5 at about twice the usual ratio. It is long only in effect.
Config: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d3_wide-uptrend-days-held-longer_1d_config.json
Criterion:
- Horizon: 6 bars
- Main measure: The sample is the non-overlapping 6-bar grid of each window, using grid bars with forecast > 0. On each, take the coin's 6-day return minus the coin's mean 6-day return over all windows. Compute the forecast-weighted mean of that excess, with its t.
- Supporting check: Split the positive-forecast grid cases at their median forecast. The mean excess 6-day return of the upper half minus the lower half must be above 0.
- Confirm: The forecast-weighted mean excess return is above 0 with t >= 2, and the supporting check passes.
- Reject: The forecast-weighted mean excess return is below 0 with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is t >= 2 when the supporting check fails, and so is any result from fewer than 100 positive-forecast grid cases across all coins and windows.
