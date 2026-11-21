---
idea: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d2_momentum-inside-90-day-rises
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: the higher a coin's 28-day return, while its 90-day return is positive -> kept
- Comparison: none
- Outcome: a higher return over the next 5 days -> kept
- Verdict transfer: yes: the config measures the 28-day return, graded, only on bars where the 90-day return is positive, and holds each bet for 5 days.
Forecast: The regime detector computes the coin's 90-bar return (`PriceEvolutionComponent`, period 90). Only bars where that return is above 0 are `trending`; every other bar is flat. On `trending` bars the forecast is the coin's 28-bar percent return (`PriceEvolutionComponent`, period 28), standardised over its past 60 values (target 10, cap 20). It is positive when the 28-day return is positive and negative when it is negative. Its size grows in proportion to that return against its usual size: a stronger 28-day gain gives a larger long, and a 28-day fall gives a short.
Config: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d2_momentum-inside-90-day-rises_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The slope of a pooled least-squares regression over all coins, with its t. It is fitted on `trending` bars of the non-overlapping 5-bar grid of each window. The regressor is the forecast (`mom28` post_pipeline_value). The response is the coin's 5-bar forward return minus the coin's normal 5-bar drift over all its windows.
- Supporting check: The book's mean daily return minus its gain from the market's own rise must be above 0, before costs.
- Confirm: The slope is positive with t >= 2, and the supporting check is above 0.
- Reject: The slope is negative with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A slope with t >= 2 whose supporting check is not above 0 is also inconclusive. So is any result with fewer than 200 grid cases on `trending` bars across all coins.
