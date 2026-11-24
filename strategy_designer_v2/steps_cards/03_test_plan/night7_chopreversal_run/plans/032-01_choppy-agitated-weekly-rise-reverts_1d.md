---
idea: 032-01_choppy-agitated-weekly-rise-reverts
brief: 032_choppy-agitated-weekly-reversal
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: a coin's 7-day rise, the larger the stronger -> kept: the 7-day return, short only while it is positive and graded by its size.
- Comparison: none -> kept
- Outcome: a fall over the next 7 days that grows with the rise -> kept: 7-bar horizon, short side, judged against the coin's normal drift.
- Verdict transfer: yes: the forecast is the idea's own rise, sized by its size, held for its 7 days inside the profile it names.
Forecast: The forecast is the coin's 7-day percent return, from PriceEvolutionComponent with period 7. It is standardised over its past 60 values (min_periods 20) and negated. It is then clipped at 0 from above. A 7-day rise therefore gives a short whose size grows with the rise, around -10 for a usual-sized rise and capped at -20. A 7-day fall or a flat week gives 0. The config uses no other condition; the code adds the choppy agitated profile around it.
Config: 032-01_choppy-agitated-weekly-rise-reverts_1d_config.json
Profile: choppy agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 7 bars
- Main measure: Use the non-overlapping 7-bar grid of each window, on bars with a forecast below 0. Measure the Pearson correlation of the forecast with the coin's next 7-bar return minus its normal 7-bar drift (the mean over all windows). Report its t.
- Supporting check: On the same cases, the mean unusual move in the signal's direction (the fall beyond the drift) is above 0.
- Confirm: The correlation is positive with t ≥ 2 (larger rises, more negative forecasts, are followed by larger falls beyond drift), and the supporting check passes.
- Reject: The correlation is negative with t ≤ -2 (larger rises are followed by larger further rises).
- Inconclusive: Any correlation t between -2 and 2, or a confirming t with a failed supporting check. Fewer than 30 grid cases with a forecast below 0, over all coins and windows, is also inconclusive.
