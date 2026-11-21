---
idea: 017-05_settlement-move-reverses-after.d2_extreme-daily-run-reverses
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a coin's 24-hour return is large relative to its usual 24-hour move -> kept: the 24-bar return divided by the hourly return volatility times sqrt(24).
- Comparison: relative to its usual 24-hour move -> kept: the volatility scaling inside the component, over a one-week (168-bar) volatility window.
- Outcome: an opposite move over the next 24 hours, larger for larger runs and concentrated in extremes -> kept: a negated position, held 24 bars, with a cubic graded dead zone.
- Verdict transfer: yes: the forecast bets against exactly the volatility-scaled 24-hour run for 24 hours, so its forward returns confirm or reject the claim.
Forecast: The forecast uses VolatilityScaledReturnComponent with period 24, vol_period 168 and vol_lookback 1. This is the last 24 hours' return in usual 24-hour moves. It is standardised against its own past 169 values (min_periods 42), so a typical run sits at about ±10. It is then negated, so the forecast is short after a rise and long after a fall. Last comes signed_power with exponent 3 and pivot 10. Runs below a typical size are damped to near zero, and the largest runs are amplified. The forecast is 0 when the 24-hour return is 0. Its size grows with the cube of how extreme the run is. It is active on every bar, with no regime gate.
Config: 017-05_settlement-move-reverses-after.d2_extreme-daily-run-reverses_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: Use non-overlapping 24-bar grid bars of each window where abs(forecast) >= 10, meaning the run is at least of typical standardised size. On each such bar, take sign(forecast) x (24-bar forward return minus the coin's mean 24-bar return over all windows). Test the mean of these values with the t of the mean, pooled over coins and windows.
- Supporting check: The same drift-adjusted, forecast-signed 24-bar return is larger on the extreme grid bars (abs(forecast) >= 10) than on the other non-zero grid bars. The check passes when the difference (extreme minus rest) is above 0.
- Confirm: The main mean is above 0 with t >= 2 over at least 30 independent cases, and the supporting difference is above 0.
- Reject: The main mean is below 0 with t <= -2 over at least 30 independent cases.
- Inconclusive: Any t between -2 and 2, or fewer than 30 extreme grid cases. A confirming main t whose supporting difference is not above 0 is also inconclusive.
