---
idea: 032-03_reversal-grows-with-choppiness
brief: 032_agitated-chop-weekly-reversal
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: b8c596b98b61
---
Fidelity:
- Situation: a coin's 7-day move scaled by its typical daily swing over the past 30 days -> kept
- Comparison: the share given back grows as the past 30 days are more agitated and trendless, meaning large daily swings against the net 30-day move -> kept: weighted by 1 − efficiency ratio over 30 days
- Outcome: part of that move is given back over the next 7 days, against its direction -> kept
- Verdict transfer: yes: the component is exactly the scaled 7-day reversal times 30-day choppiness, so its forward payoff, and how that payoff grows with choppiness, test the idea directly.
Forecast: One indicator, ChoppinessWeightedScaledReversalComponent (period 7, vol_period 30, er_period 30). It is minus the 7-day return divided by the 30-day daily-return standard deviation times √7, multiplied by (1 − the raw 30-day Kaufman efficiency ratio). It is standardised over its past 60 values (min 20), so its average size is about 10, capped at ±20. The forecast is positive (long) after a 7-day fall and negative (short) after a 7-day rise. It grows with the size of the move in usual swings and with how choppy the past 30 days were. It is near 0 after a small move or a clean straight-line 30-day trend. There is no gate, because the idea is a steady graded relation.
Config: 032-03_reversal-grows-with-choppiness_1d_config.json
Criterion:
- Horizon: 7 bars
- Main measure: Use a non-overlapping 7-bar grid in each window. At each grid bar, take the coin's next-7-bar return minus its normal 7-bar drift (its mean over all windows), so the coin's own rise is not credited. Regress that excess return on the bar's forecast (post_pipeline_value), pooling all coins and windows. Report the slope's t, with same-day cases summed as one piece of evidence.
- Supporting check: Recompute 1 − ER(30) and the scaled 7-day move from the recorded closes on the same grid bars. The slope of the next-7-bar excess return on minus the scaled move must be larger in the upper half of 1 − ER than in the lower half (difference upper minus lower > 0).
- Confirm: Main slope positive with t ≥ 2 (larger forecasts are followed by larger moves in their direction), and the supporting check's difference is above 0.
- Reject: Main slope negative with t ≤ −2, meaning the 7-day move continues, or reverses less the choppier the market.
- Inconclusive: Any t between −2 and 2, or a confirming main slope whose supporting difference is not above 0. At least 200 grid cases with a nonzero forecast, spread over at least 100 distinct days.
