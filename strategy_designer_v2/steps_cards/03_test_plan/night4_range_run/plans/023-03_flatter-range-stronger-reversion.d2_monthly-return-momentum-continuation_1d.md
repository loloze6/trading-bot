---
idea: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: be08f97ea86e
---
Fidelity:
- Situation: a coin's 30-day return, larger meaning stronger -> kept: 30-bar percent return, signed and graded.
- Comparison: none -> kept
- Outcome: a larger rise over the next 5 days, for a larger 30-day return -> kept: the 5-bar forward return, held 5 bars.
- Verdict transfer: yes: the forecast is the 30-day return itself, and the test checks whether 5-day returns grow with it.
Forecast: The forecast is the coin's 30-bar percent return (PriceEvolutionComponent, period 30), standardised against its own last 60 values (min 20). It is used on every bar, with no regime. It is positive after a 30-day rise and negative after a 30-day fall. Its size grows in proportion to the size of the return, against its usual size, capped at ±20. It is zero only when the 30-day return is zero.
Config: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The slope of the coin's excess 5-bar forward return on the forecast at bar t, pooled over all coins and windows. The excess return is close[t+5]/close[t] − 1 minus that coin's mean 5-bar return over all its windows. The bars t are the non-overlapping grid positions 0, 5, 10, ... of each window.
- Supporting check: none
- Confirm: The slope is positive with a t of 2 or more, over at least 200 grid cases. That means larger 30-day returns are followed by larger 5-day rises than the coin's drift.
- Reject: The slope is negative with a t of −2 or less, over at least 200 grid cases. That means larger 30-day returns are followed by smaller 5-day moves than the drift.
- Inconclusive: The idea is neither confirmed nor rejected in two cases: - the t lies between −2 and 2, including a slope near zero; - there are fewer than 200 non-overlapping grid cases with a recorded forecast.
