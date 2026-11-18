---
idea: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation
brief: 006_range-compression-precedes-expansion
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: the coin's 10-day return measured against its own 20-day volatility, and how strong it is -> kept
- Comparison: the price rise judged against the coin's usual 3-day return -> kept
- Outcome: the price rises over the next 3 days, more after stronger advances and most after the strongest -> adapted: the strength of the advance is graded, and a convex dead zone concentrates the position on the strongest advances
- Verdict transfer: yes: the forecast is the idea's own volatility-scaled 10-day advance, so a 3-day excess rise after its largest values confirms the idea and a 3-day excess fall rejects it.
Forecast: One indicator, VolatilityScaledReturnComponent with period 10 and vol_period 20. It gives the 10-day return divided by (the 20-day standard deviation of daily returns x sqrt(10)). That value is standardised against its own past 60 values (min_periods 20). It is then clipped at 0, so only advances count and the forecast is long-only, as the idea's consequence says. Last, signed_power with exponent 3 and pivot 10 is applied. The forecast is 0 when the 10-day return is zero or negative. It is small for ordinary advances (an advance of half the usual size gives about 1.25). It grows cubically for advances stronger than usual: a standardised 15 becomes about 34, and the combined forecast is capped at 20. It is never negative.
Config: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: Use the non-overlapping 3-bar grid of each window. Take the grid bars whose forecast is in the top 20% of all grid bars with forecast > 0, pooled over the coins. On those bars, compute the coin's 3-bar return minus that coin's mean 3-bar return over all windows. Test the mean of this excess return with a one-group t.
- Supporting check: On the grid bars, the top-group mean excess 3-bar return minus the mean excess 3-bar return on bars with forecast 0. This difference must be greater than 0.
- Confirm: The top-group mean excess return is above 0 with t >= 2, and the supporting difference is above 0.
- Reject: The top-group mean excess return is below 0 with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t of 2 or more with a supporting difference of 0 or less is also inconclusive. At least 100 grid bars are required in the top group; with fewer, the test is inconclusive.
