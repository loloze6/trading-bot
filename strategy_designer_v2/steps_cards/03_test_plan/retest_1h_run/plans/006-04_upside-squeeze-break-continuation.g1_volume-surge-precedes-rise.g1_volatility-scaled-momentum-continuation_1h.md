---
idea: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation
brief: 006_range-compression-precedes-expansion
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 1f000a7ba652
---
Fidelity:
- Situation: the 10-day return measured against the coin's own 20-day volatility -> kept: one-bar return volatility over 480 bars scales the 240-bar return.
- Comparison: next 3-day rise against the coin's usual 3-day return -> kept: forward 72-bar return minus the coin's mean 72-bar return over all windows.
- Outcome: the price rises more the stronger the advance, mostly after the strongest ones -> kept: the long position grows with the scaled advance, with a graded dead zone.
- Verdict transfer: yes: the forecast is the idea's own measure, so a top-position excess return confirms or refutes the idea directly.
Forecast: One component, VolatilityScaledReturnComponent with period 240 (10 days) and vol_period 480 (20 days). It gives the 240-bar return divided by the 480-bar standard deviation of hourly returns times sqrt(240). It is standardised against its own past 481 values (min_periods 120) and clipped at 0, so a falling coin gives a flat position. A signed_power with exponent 3 then damps ordinary advances towards 0 and amplifies the strongest ones. The forecast is 0 when the 10-day return is zero or negative, small for moderate advances, and grows steeply with the volatility-scaled advance, up to the +20 cap.
Config: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: On each window's non-overlapping 72-bar grid, take the cases in the top quintile of forecast among bars with forecast > 0, pooled over coins. For each case, compute close[t+72]/close[t]-1 minus that coin's mean 72-bar return over all windows. Report the mean of this excess and its t (ordinary t of the mean).
- Supporting check: The excess return mean of the top-quintile cases minus that of the other forecast > 0 cases is positive, by Welch's t.
- Confirm: The main measure has a mean excess > 0 with t ≥ 2. The check must also pass, with a Welch difference > 0 and t ≥ 1.
- Reject: The top-quintile mean excess has t ≤ -2.
- Inconclusive: The idea is neither confirmed nor rejected when the main t lies between -2 and 2, or when the main measure confirms but the check fails. The test also needs at least 150 top-quintile cases pooled, with at least 15 per coin. Below that it is inconclusive.
