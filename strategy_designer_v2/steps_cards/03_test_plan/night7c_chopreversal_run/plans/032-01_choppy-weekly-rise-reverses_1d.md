---
idea: 032-01_choppy-weekly-rise-reverses
brief: 032_agitated-chop-weekly-reversal
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 051b3422f169
---
Fidelity:
- Situation: a coin choppy over 30 days, with large two-way daily swings and little net progress -> adapted: a regime where the 30-day efficiency ratio is at most 0.3 and 30-day volatility ranks at or above its 365-day median.
- Comparison: the 7-day rise against the typical daily swing of the past 30 days -> kept: the 7-day return divided by the 30-day standard deviation of daily returns.
- Outcome: partly given back with a decline over the next 7 days, larger for larger rises -> adapted: a graded short that grows with the scaled rise, held 7 bars.
- Verdict transfer: yes: the test measures the same regime, the same scaled rise and the same 7-day decline, so a confirm or a reject carries over to the idea.
Forecast: The forecast is non-zero only on bars the detector labels mean_reversion. That happens when the raw 30-day efficiency ratio is at most 0.3 (choppy) and the 30-day volatility ranks at or above 0.5 of its past 365 days (agitated). In that regime the forecast is built from the 7-day return divided by (30-day std of daily returns x sqrt 7). It is standardised against its own past 60 values, negated and clipped at 0. It is therefore a short that grows with the size of the scaled 7-day rise, 0 after a 7-day fall, and 0 outside the regime.
Config: 032-01_choppy-weekly-rise-reverses_1d_config.json
Criterion:
- Horizon: 7 bars
- Main measure: Use the cases: bars on the 7-bar grid of each window where the forecast is below 0. For each case, take the coin's 7-bar return minus its normal 7-bar drift (the mean over all windows), signed in the short direction. The measure is the mean of this unusual move, with its t computed with cases on the same day taken together.
- Supporting check: The rank correlation between |forecast| and the short-signed unusual move over the same cases is above 0.
- Confirm: The mean short-signed unusual move has t ≥ 2, and the supporting rank correlation is above 0.
- Reject: The mean short-signed unusual move has t ≤ -2, meaning the rise continues.
- Inconclusive: A t between -2 and 2 is inconclusive. A positive main measure with a rank correlation of 0 or below is also inconclusive. Fewer than 30 cases, or cases on fewer than 30 distinct days, is inconclusive.
