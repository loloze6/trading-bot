---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 69ac1b38a672
---
Fidelity:
- Situation: a day that closes lower, with its high-low range above the coin's 30-day average range -> adapted: "closes lower" is a regime; the range over its 30-day mean range is graded, not a threshold.
- Comparison: that day's range against the coin's average range over the past 30 days -> kept
- Outcome: the coin's return over the next 3 days is higher than its usual drift, more so the wider the day -> kept
- Verdict transfer: yes: the same falling-day gate, range ratio and 3-day excess return are measured as the idea states them.
Forecast: The forecast is computed only on days that close below the prior close. A regime rule on the 1-day price change (below 0) selects these days. Every other day is flat. On a falling day the forecast is the mean of two parts. The first part is the day's high-low range divided by the mean daily high-low range of the last 30 days, standardised. That puts it near +10 at an average-width day and up to +20 for a very wide one. The second part is a constant of -10. So the forecast is (x - 10) / 2. It is 0 when the day's range equals its usual level. It is positive and grows up to about +5 as the falling day gets wider than usual. It is mildly negative when a falling day is narrower than usual.
Config: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: Use falling-day bars (regime mean_reversion) on a non-overlapping 3-bar grid per window. Regress each case's 3-day return minus the coin's mean 3-day return over all windows (the excess return) on the bar's forecast, all coins pooled. The measure is the t of the slope.
- Supporting check: Take the cases in the top third of forecast. Their mean excess 3-day return must be above 0.
- Confirm: The slope t is 2 or more, and the top-third mean excess return is positive.
- Reject: The slope t is -2 or less.
- Inconclusive: A slope t between -2 and 2 is inconclusive. A slope t of 2 or more with a top-third mean of 0 or below is also inconclusive. Fewer than 300 falling-day grid cases is no verdict.
