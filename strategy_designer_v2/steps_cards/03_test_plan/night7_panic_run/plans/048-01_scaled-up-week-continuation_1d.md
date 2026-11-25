---
idea: 048-01_scaled-up-week-continuation
brief: 048_scaled-week-moves-continue-both-ways
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 18d3cc56dd45
---
Fidelity:
- Situation: a week in which the coin rose -> kept: the 7-day return is above 0; the forecast is 0 on every bar where it is not.
- Comparison: the 7-day return in units of the 30-day standard deviation of daily returns -> kept: VolatilityScaledReturnComponent(7, 30) is that ratio, up to the constant sqrt(7).
- Outcome: the price keeps rising over the next 3 days, more so the larger the scaled return -> adapted: "after a week" made "while the past week rose", graded by the scaled return, with the bet held 3 bars.
- Verdict transfer: yes: the forecast is exactly the idea's scaled up-week size, and it is judged on the next 3 days' excess return.
Forecast: The forecast uses one indicator: the coin's 7-bar return divided by (the standard deviation of its last 30 daily returns x sqrt 7). It is standardised against its own last 60 values (min 20) and clipped at 0. It is positive and grows linearly with the up-week's size in swing units. It is 0 whenever the last 7 days did not rise, so the strategy is long-only. Its average active size is about 10, capped at 20.
Config: 048-01_scaled-up-week-continuation_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: The slope of the coin's next 3-bar return, minus its normal 3-bar drift (its mean over all windows), on the forecast. It uses non-overlapping 3-bar grid bars of each window where the forecast is above 0, pooling coins. Its t clusters cases of the same day together.
- Supporting check: On those same cases, the mean excess 3-bar return in the long direction (the unusual move) is above 0.
- Confirm: Slope t of 2 or more, and the supporting check passes (mean excess return above 0).
- Reject: Slope t of -2 or less.
- Inconclusive: A slope t between -2 and 2, or a slope t of 2 or more with a mean excess return of 0 or below. At least 200 grid cases with a positive forecast, on at least 100 distinct days, are needed; below that the result is inconclusive.
