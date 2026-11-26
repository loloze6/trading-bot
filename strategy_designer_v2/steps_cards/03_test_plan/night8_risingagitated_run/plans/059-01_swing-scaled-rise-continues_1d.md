---
idea: 059-01_swing-scaled-rise-continues
brief: 059_swing-scaled-weeks-move-continues-anywhere
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 4510fe2da56d
---
Fidelity:
- Situation: the coin's 20-day return divided by the standard deviation of its daily returns over the same 20 days -> kept: `VolatilityScaledReturnComponent` with period 20 and vol_period 20 (its constant √20 cancels under standardise).
- Comparison: the coin's own daily swing over those 20 days -> kept: it is the divisor in the same component.
- Outcome: the larger that scaled rise, the larger the rise over the next 5 days (and a scaled fall, a fall) -> kept: a signed forecast graded by the scaled move, held 5 bars.
- Verdict transfer: yes: the forecast is the idea's scaled move itself, so its link to the next 5 days' return is the idea's claim.
Forecast: One component: the 20-day return divided by the standard deviation of the last 20 daily returns, all ending at today's close. It is standardised against its own last 60 values (min 20), so its average absolute size is about 10, capped at ±20. The forecast is that value alone, ungated. It is positive after a 20-day rise and negative after a 20-day fall, and zero only when the 20-day move is zero. It grows linearly with the size of the move in units of the coin's own daily swing.
Config: 059-01_swing-scaled-rise-continues_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The slope (with its t) of a regression of excess return on the forecast. The excess return is the coin's next-5-bar return minus its normal 5-bar drift, which is its mean 5-bar return over all its windows. The forecast is the one recorded at that bar's close. Samples are taken on a non-overlapping 5-bar grid inside each window, all coins pooled, before costs.
- Supporting check: none
- Confirm: The slope is positive with t ≥ 2 over at least 300 grid cases.
- Reject: The slope is negative with t ≤ -2 over at least 300 grid cases, meaning larger scaled moves are followed by reversal.
- Inconclusive: These results neither confirm nor reject: - a t between -2 and 2, including slopes near zero; - fewer than 300 grid cases.
