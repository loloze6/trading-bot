---
idea: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins.b2_thirty-day-return-continuation
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: e48527ec0eac
---
Fidelity:
- Situation: a coin's 30-day return, the larger the stronger -> kept
- Comparison: larger 30-day returns against smaller ones -> kept
- Outcome: a larger rise over the next 10 days -> kept
- Verdict transfer: yes: the forecast is the 30-day return itself, held 10 days, so a graded relation to the 10-day move confirms or rejects the idea directly.
Forecast: One component, the 30-bar percent price change (`PriceEvolutionComponent`, period 30), standardised against its own past 60 values (min 20). The forecast is positive after a 30-day rise and negative after a 30-day fall. It is zero when the 30-day return is zero. It grows in proportion to the size of the return, about ±10 at a usual-sized move and capped at ±20. No regime is used, and every bet is held 10 bars.
Config: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins.b2_thirty-day-return-continuation_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Use the non-overlapping 10-bar grid of each window, pooled over coins and windows. At each grid bar, take the coin's 10-bar forward return minus that coin's mean 10-bar return over all its windows (holding the coin). Regress this excess return on the bar's `forecast`, and report the t of the slope.
- Supporting check: none
- Confirm: The slope is positive with t ≥ 2.
- Reject: The slope is negative with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. So are fewer than 300 grid cases with a recorded forecast.
