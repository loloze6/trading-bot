---
idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d2_moderate-hourly-shocks-reverse-daily
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a coin's last 1-hour return, measured against its 24-hour volatility -> kept
- Comparison: only moves of up to a few times that volatility, not the most extreme ones -> kept: a regime veto sends bars beyond ±3 usual moves to flat
- Outcome: the next 24-hour return runs the opposite way, more so for a larger shock -> kept
- Verdict transfer: yes: the forecast is the faded vol-scaled hourly shock, limited to moderate shocks and held 24 hours, which is exactly the idea's claim.
Forecast: The raw value is the last 1-hour return divided by the standard deviation of the last 24 hourly returns (VolatilityScaledReturnComponent, period 1, vol_period 24). It is standardised over 60 bars and negated, so the forecast fades the move. After an up-shock it is negative (short), after a down-shock it is positive (long), and its size grows in proportion to the shock. A regime veto sets the forecast to 0 (flat) on bars where the scaled shock is 3 usual moves or more in either direction. Those are the extreme moves the idea says do not reverse.
Config: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d2_moderate-hourly-shocks-reverse-daily_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: Cases are the bars at positions 0, 24, 48, … of each window where the forecast is not 0. For each case, x = forecast/10 × (close[t+24]/close[t] − 1 − the coin's mean 24-bar return over all windows). The measure is the t of the mean of x over all cases, before costs.
- Supporting check: Rank the cases by |forecast| into thirds. The mean drift-removed 24-bar return in the forecast's direction must be higher in the top third than in the bottom third.
- Confirm: The main t is 2 or more and the top third beats the bottom third.
- Reject: The main t is −2 or less.
- Inconclusive: Any of these is inconclusive: - the main t is between −2 and 2; - the main t is 2 or more but the top third does not beat the bottom third; - there are fewer than 500 cases with a nonzero forecast.
