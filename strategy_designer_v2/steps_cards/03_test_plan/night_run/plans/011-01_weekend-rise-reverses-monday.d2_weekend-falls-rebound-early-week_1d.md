---
idea: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the coin fell over the weekend, Saturday-to-Sunday close-to-close, sized against its usual daily move -> adapted: the threshold "fell" is made graded, using the Sunday bar's return over its 20-day volatility (kept only on its falling side).
- Comparison: the weekend fall relative to the coin's usual daily move -> kept: the return is divided by the standard deviation of the last 20 daily returns.
- Outcome: the price rises over the next 3 days, more after larger falls -> adapted: holding period dropped, so the position is set at Sunday's close and the 3-day rise is measured from the record.
- Verdict transfer: yes: the measure is Sunday-close-to-Wednesday-close returns against the size of the weekend fall, which is exactly what the idea claims.
Forecast: The forecast is active only at Sunday's close, when the WeekdayComponent says the coming bar is Monday. On other days the regime is null and the forecast is flat. The indicator is the Sunday bar's one-day return divided by the standard deviation of the last 20 daily returns (VolatilityScaledReturnComponent, period 1, vol_period 20). It is standardised over the 60 previous daily values and its sign is flipped, so a fall becomes positive. It is then clipped at 0 from below. The forecast is zero after a weekend rise and positive after a weekend fall, and it grows linearly with the size of the fall in usual moves, capped at 20. It is long-only because the idea speaks only of falls.
Config: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: Use the Sunday bars, which are the bars with regime "trending", one per week, so they never overlap. On each, take the 3-bar return from Sunday's close to Wednesday's close, inside the window. Subtract the coin's mean 3-bar return over all its windows. Regress this excess return on the bar's forecast, pooled over coins and windows, and report the OLS slope's t.
- Supporting check: Take the Sunday bars with forecast > 0. Their forecast-weighted mean excess 3-bar return must be greater than 0.
- Confirm: The slope's t is 2 or more, and the supporting check is positive.
- Reject: The slope's t is -2 or less.
- Inconclusive: A t between -2 and 2 is inconclusive, as is a confirm-strength slope whose check fails. The test needs at least 300 Sunday bars with forecast > 0 and 600 Sunday bars in total; below that the result is inconclusive.
