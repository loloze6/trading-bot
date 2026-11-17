---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins.g1_falling-month-keeps-falling
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: the coin's close sits further below its 60-day high, while its 30-day return is negative -> kept
- Comparison: the next 7-day return relative to the coin's own average return -> kept
- Outcome: the 7-day return is lower (worse than the coin's average) the deeper the close is below the high -> kept
- Verdict transfer: yes: the test measures this same graded depth, under this same falling-month condition, against this same 7-day outcome relative to the coin's average.
Forecast: The regime detector reads the 30-day price change (PriceEvolutionComponent, period 30). On bars where it is below 0, the bar is `mean_reversion`; every other bar is `unknown` and flat. In the falling-month regime, the forecast is the 60-day distance from high (DistanceFromHighComponent, period 60), standardised over its past 60 values (min 20). That distance is 0 at a new high and more negative the deeper the close is below it. The forecast is therefore 0 or negative only. It is near 0 when the close is just under its 60-day high, and the short position grows in step with the depth below the high, up to -20. There is no dead zone, because the idea covers the whole range of ordinary declines.
Config: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins.g1_falling-month-keeps-falling_1d_config.json
Criterion:
- Horizon: 7 bars
- Main measure: Use the bars of the falling-month regime (regime = mean_reversion) that fall on the non-overlapping 7-bar grid of each window. On those bars, take the pooled OLS slope of the excess 7-bar return on the recorded forecast. The excess return is the coin's 7-bar return minus that coin's mean 7-bar return over all its windows. Report the slope with its t and the number of cases.
- Supporting check: On the same cases, the mean of (forecast / 10) × excess 7-bar return must be above 0. This is the timing gain of the short against simply holding the coin.
- Confirm: The slope is positive with t ≥ 2: a deeper fall below the high gives a lower excess return. The supporting check must also pass.
- Reject: The slope is negative with t ≤ -2: a deeper fall below the high gives a higher excess return.
- Inconclusive: These results neither confirm nor reject: - any slope with -2 < t < 2; - t ≥ 2 while the timing gain is not above 0; - fewer than 100 grid cases in the regime across all coins and windows.
