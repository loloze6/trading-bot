---
idea: 022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: a coin's 28-day return, higher or lower -> kept
- Comparison: higher 28-day return against lower, across its graded levels -> kept
- Outcome: the next 5 days' return is higher when the 28-day return is higher -> kept
- Verdict transfer: yes: the forecast is the coin's own 28-day return, and it is judged against its 5-day forward return.
Forecast: The forecast is the coin's 28-bar percent return (PriceEvolutionComponent, period 28), standardised against its own last 60 values (min_periods 20). It is positive and grows with a stronger 4-week rise, and negative and grows with a deeper 4-week fall. It is never short while the 4-week return is positive, so it takes no short against a rise. It is near zero when the 28-day return is near zero. It is active on every bar, with no regime.
Config: 022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: On each window's non-overlapping 5-bar grid, take the coin's 5-day forward return minus the coin's mean 5-day return over all its windows. Regress that excess return on the forecast (post_pipeline_value of mom28), pooled over coins and windows. The result is the slope's t-statistic.
- Supporting check: The mean excess 5-day return of grid cases in the top fifth of forecasts, minus that of the bottom fifth, is above 0.
- Confirm: The slope's t is 2 or more, and the top-minus-bottom-fifth difference is above 0.
- Reject: The slope's t is -2 or less.
- Inconclusive: A slope t between -2 and 2 is inconclusive. A t of 2 or more with a top-minus-bottom difference of 0 or less is also inconclusive. A result needs at least 300 independent grid cases with a recorded forecast; fewer is inconclusive.
