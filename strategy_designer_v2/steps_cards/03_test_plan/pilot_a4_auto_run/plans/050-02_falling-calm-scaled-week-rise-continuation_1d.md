---
idea: 050-02_falling-calm-scaled-week-rise-continuation
brief: 050_calm-downtrend-scaled-weeks-continue
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: bd33e939b067
---
Fidelity:
- Situation: in a falling, calm market, the coin has risen over the last 7 days -> kept: the profile is added by code, and the 7-day return is clipped at 0, so the book is flat when the coin has not risen.
- Comparison: the 7-day rise in units of the 30-day daily-return swing -> kept: VolatilityScaledReturnComponent, with the constant sqrt(7) cancelled by standardise.
- Outcome: keeps rising over the next 3 days, further for a larger scaled rise -> kept: long, graded by the scaled rise, held 3 bars.
- Verdict transfer: yes: the forecast is exactly the idea's scaled 7-day rise, long only inside the profile, judged over the idea's 3-day horizon.
Forecast: The forecast is computed on every bar inside the falling calm profile. It takes the coin's 7-day return divided by sqrt(7) times the standard deviation of its last 30 daily returns, using VolatilityScaledReturnComponent with period 7 and vol_period 30. That value is standardised against its own last 60 values (min_periods 20), so a usual-size move reads about 10, capped at 20. It is then clipped at 0. The forecast is therefore 0 when the coin fell or was flat over 7 days, and positive and growing linearly with the scaled rise when it rose. It is never negative.
Config: 050-02_falling-calm-scaled-week-rise-continuation_1d_config.json
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: A case is a rise of the forecast of at least 2 points, read once per 3-bar grid cell of each window. Per case, take the coin's 3-day return from the signal bar's close minus the coin's mean 3-day return over all windows. The measure is the mean of this unusual move over the cases, with its t computed with cases of the same day summed together.
- Supporting check: Split the cases at the median of their forecast. Take the mean unusual move of the upper half minus that of the lower half, with Welch's t.
- Confirm: The idea is confirmed only when both hold: - the main measure's mean unusual move is positive with t >= 2; - the supporting difference (upper half minus lower half) is positive with t >= 2.
- Reject: The idea is rejected when either holds: - the main measure's mean unusual move has t <= -2 (a reversal); - the supporting difference has t <= -2 (the carry-on shrinks with size).
- Inconclusive: Any other result is inconclusive, including a main t between -2 and 2, or a confirming main measure with a supporting t between -2 and 2. Fewer than 40 cases in total, or fewer than 20 in either half, is also inconclusive.
