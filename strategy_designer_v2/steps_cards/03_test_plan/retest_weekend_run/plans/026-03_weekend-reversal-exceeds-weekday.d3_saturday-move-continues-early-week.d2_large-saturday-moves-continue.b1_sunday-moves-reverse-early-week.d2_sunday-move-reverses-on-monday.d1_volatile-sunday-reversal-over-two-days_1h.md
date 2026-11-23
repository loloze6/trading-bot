---
idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.d1_volatile-sunday-reversal-over-two-days
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a coin's 24-hour return over Sunday, measured against its usual 30-day move -> kept: the 24h return at Sunday's last hourly close, divided by the mean absolute 24h return over 720 bars.
- Comparison: Sunday's move against the coin's usual 30-day move -> kept: the same divisor of 720 bars.
- Outcome: over Monday and Tuesday (next 48 hours), a move against Sunday's, larger in % of price when 30-day hourly volatility is higher -> kept: the 48-bar return after the entry, and its size by 30-day hourly volatility, measured in the criterion.
- Verdict transfer: yes: the forecast leans against Sunday's scaled move only at Sunday's close, the bet is held 48 bars, and the criterion tests both the reversal and its growth with volatility.
Forecast: A calendar regime is active only on the bar whose next bar opens Monday 00:00 UTC, which is the last hour of Sunday. On that bar the forecast comes from MeanAbsScaledReturnComponent (period 24, window 720). This is Sunday's 24h return in units of the coin's usual 24h move over 30 days. It is standardised (window 500, min_periods 120) and negated. The forecast is short after a Sunday rise and long after a Sunday fall, and its size grows linearly with the size of Sunday's move against its usual size. On every other bar the forecast is 0, and the 48-bar holding period keeps the bet through Tuesday. The engine's own volatility sizing cannot make the stake rise with volatility, so that part of the idea is tested in the criterion, not built into the stake.
Config: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.d1_volatile-sunday-reversal-over-two-days_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: The cases are the entry bars: regime mean_reversion with a forecast that is not zero, one per coin per week, so cases do not overlap. For each case, take the coin's 48-bar return from the entry close minus the coin's normal 48-bar drift (its mean over all windows). Fit a pooled least-squares slope of this excess return on the forecast, and take the t of that slope.
- Supporting check: For each case, compute the 30-day hourly volatility from the record's closes: the std of the 720 one-bar returns before the entry, inside the window. Split the cases into the top and bottom thirds of each coin's volatility. In each third, fit the slope of the excess 48-bar return in % of price on the forecast. Measure the top-third slope minus the bottom-third slope, with Welch's t.
- Confirm: The main slope is positive with t ≥ 2, and the supporting-check difference is positive with t ≥ 2.
- Reject: Either the main slope is negative with t ≤ -2 (Sunday's move continues), or the supporting-check difference is negative with t ≤ -2 (the reversal is smaller in volatile months).
- Inconclusive: Any other result counts as inconclusive, including slopes near zero and t values between -2 and 2. The test also needs at least 300 cases across all coins and at least 100 cases in each volatility third; with fewer cases the result is inconclusive.
