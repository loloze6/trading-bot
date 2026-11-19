---
idea: 016-03_up-jump-price-reversal
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 1f000a7ba652
---
Fidelity:
- Situation: the coin has risen over the past 3 days, and a share of that rise came from its few biggest hourly gains -> kept: the rise is a regime rule (72-bar return > 0), and the share is the top-3 hourly gains over the 72-bar net rise.
- Comparison: a larger biggest-gains share against a smaller one -> kept: the short position grows continuously with the share.
- Outcome: the more of the rise the coin gives back over the next 3 days (falls) -> kept: next 72-bar return, and the fall as a fraction of the past rise.
- Verdict transfer: yes: the forecast is the share itself, active only after a 3-day rise and short, so its fit with the next 72 bars' fall is the idea's claim.
Forecast: A regime rule marks bars where the 72-bar price change is positive (`trending`). Every other bar is flat (`null`). On those bars the forecast is short. Its size is TopGainsShareOfRise(period 72, k 3): the 3 largest hourly gains over the net 72-hour rise, capped at 1. That share is standardised against its own past 73 values (about 10 on average, capped at 20) and then negated. It is near 0 when the rise is a grind of many small hours. It is about -10 to -20 when a few hours carry all of the rise.
Config: 016-03_up-jump-price-reversal_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: Sample the non-overlapping 72-bar grid of each window and keep the bars whose regime is `trending`. On those bars, regress the coin's excess next-72-bar return on the forecast. The excess return is close[t+72]/close[t]-1 minus that coin's mean 72-bar grid return over all windows. Report the t of the slope (OLS) and the number of cases.
- Supporting check: On the same bars, regress the giveback fraction on |forecast|. The giveback fraction is -(close[t+72]/close[t]-1) divided by (close[t]/close[t-72]-1). Its slope must be positive.
- Confirm: The main slope is positive with t ≥ 2: more negative forecasts, meaning larger jump shares, are followed by lower excess returns. The supporting slope must also be positive.
- Reject: The main slope is negative with t ≤ -2: larger jump shares are followed by higher excess returns.
- Inconclusive: Any main t between -2 and 2. Also a main t ≥ 2 when the supporting slope is not positive. At least 100 grid cases across coins and windows are required; below that the result is inconclusive.
