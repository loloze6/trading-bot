---
idea: 020-01_resistance-retest-turns-down.d2_thirty-day-momentum-continues
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: e48527ec0eac
---
Fidelity:
- Situation: a coin's 30-day return, larger meaning stronger -> kept
- Comparison: larger versus smaller 30-day returns ("the larger ..., the more") -> kept
- Outcome: the coin rises more over the next 5 days -> kept
- Verdict transfer: yes: the forecast is the 30-day return itself, and the test asks whether 5-day returns grow with it.
Forecast: The forecast is one component, PriceEvolutionComponent with period 30: the percent change of the close over the last 30 daily bars. It is standardised against its own past 60 values (min_periods 20), so a typical move reads about ±10, capped at ±20. The forecast is positive after a 30-day rise and negative after a 30-day fall. Its size grows continuously with the size of the move, and it is zero only when the 30-day return is zero. It is ungated and active on every bar.
Config: 020-01_resistance-retest-turns-down.d2_thirty-day-momentum-continues_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Regress each coin's 5-bar forward return, minus that coin's normal 5-bar drift (its mean over all windows), on the forecast. Use the non-overlapping 5-bar grid of each window, pool all coins and windows, and report the t of the slope (OLS).
- Supporting check: The book's mean daily return before costs, minus its gain from the market's own rise, is above 0.
- Confirm: The slope's t is 2 or more, and the book's timing gain is above 0.
- Reject: The slope's t is -2 or less.
- Inconclusive: A t between -2 and 2, or a t of 2 or more with a timing gain of 0 or less. The test needs at least 300 non-overlapping grid cases with a recorded forecast; with fewer, the result is inconclusive.
