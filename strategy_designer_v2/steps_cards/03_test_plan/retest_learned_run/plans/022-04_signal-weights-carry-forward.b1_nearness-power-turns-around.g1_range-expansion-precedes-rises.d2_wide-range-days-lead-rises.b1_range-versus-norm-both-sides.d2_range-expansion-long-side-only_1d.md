---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d2_range-expansion-long-side-only
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 69ac1b38a672
---
Fidelity:
- Situation: a coin's daily high-low range exceeds its 30-day average range, the further the stronger -> kept
- Comparison: the coin's usual drift over 3 days, with no lean against the coin after narrower days -> kept
- Outcome: the coin's return over the next 3 days is higher, long side only -> kept
- Verdict transfer: yes: the forecast is today's range against its 30-day mean range, long and graded above the mean, zero below it, and it is judged on 3-day returns in excess of the coin's drift.
Forecast: The forecast uses one indicator, RangeCompressionRatioComponent with short_period 1, long_period 30, base "mean_bar_range" and form "compression". Its value is 1 minus (today's high-low range divided by the mean high-low range of the last 30 days, today included). The forecast standardises that value over its past 60 values, which keeps a zero at a day of average width. It then negates it, so the forecast is positive when today is wider than average. It then clips it at 0, so the side is long only. The forecast is zero on days at or below the average range. It is positive and grows in proportion to how far today's range exceeds the 30-day mean, about +10 for a typical excess, capped at +20. It is never negative.
Config: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d2_range-expansion-long-side-only_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: Use the non-overlapping 3-bar grid of each window, on grid bars with forecast > 0. On each bar, take the coin's 3-bar forward return minus the coin's mean 3-bar return over all its windows. Measure the forecast-weighted mean of that excess return, sum(forecast x excess) / sum(forecast), with the t of the per-bar products forecast x excess.
- Supporting check: none
- Confirm: The forecast-weighted mean excess 3-bar return is above 0 with t >= 2, over at least 100 independent grid cases pooled across coins and windows.
- Reject: The forecast-weighted mean excess 3-bar return is below 0 with t <= -2, over at least 100 independent grid cases.
- Inconclusive: Any t between -2 and 2 is inconclusive, including an estimate near zero. Fewer than 100 independent grid cases with forecast > 0 are also inconclusive, whatever the t.
