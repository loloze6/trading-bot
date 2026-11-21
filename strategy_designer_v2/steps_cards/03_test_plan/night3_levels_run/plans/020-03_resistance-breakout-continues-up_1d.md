---
idea: 020-03_resistance-breakout-continues-up
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: d79aab634da6
---
Fidelity:
- Situation: a close above a price where the coin turned down several times in the past 90 days -> adapted: the "several times" threshold is made graded as the touch count N of the crossed swing-high level times the close's percent margin above it, using ResistanceBreakTouchCountComponent (90 bars, cross on this bar).
- Comparison: the more times the level held before, the larger the rise -> kept: the forecast grows with the level's touch count N.
- Outcome: price keeps rising over the next 5 days -> kept: each long bet is held 5 daily bars, and we measure the 5-bar return after it.
- Verdict transfer: yes: the forecast is long only on closes through recently crossed, repeatedly held levels and grows with their touch count, so a 5-day continuation measured after these cases confirms or rejects the idea itself.
Forecast: The forecast uses one component, ResistanceBreakTouchCountComponent (period 90, side 2, band 2.0, cross_period 1). - Raw value: on a bar whose close crosses above a swing-high close (a past turn down) from at or below it on the prior bar, the value is N x (close − level) / level x 100. N is the number of turns down within 2 % of that level in the last 90 bars. On every other bar it is 0. - Scaling: the value is standardised against its own past 90 values (min_periods 22). It is then passed through signed_power with exponent 3 and pivot 10, a graded dead zone. Weak breaks (a single touch, a tiny margin) are damped smoothly towards 0, and strong breaks of often-held levels are amplified up to the cap. - Sign: the forecast is never negative, because the raw value is never negative. It is 0 when no held level was just broken. It is larger with more touches and a clearer close above the level. - Gating: none, so every bar resolves to the "unknown" regime.
Config: 020-03_resistance-breakout-continues-up_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The measure is taken over cases, where a case is a rise of the forecast of at least 2 points, read once per 5-bar grid cell of each window. - Per case: the coin's return from the case bar's close over the next 5 bars, inside the window, minus the coin's normal 5-bar drift (its mean 5-bar return over all its windows). - Result: the mean of these excess returns, pooled over all coins and windows, with its ordinary t.
- Supporting check: Split the cases at the median of the component's raw value (last_history_value, N x margin) on the case bar. The mean excess return of the top half minus that of the bottom half must be above 0.
- Confirm: The idea is confirmed when both hold: - the mean excess 5-bar return is positive with t ≥ 2, over at least 30 cases; - the supporting check passes.
- Reject: The mean excess 5-bar return is negative with t ≤ −2, over at least 30 cases.
- Inconclusive: Any of these results is inconclusive: - t strictly between −2 and 2; - t ≥ 2 but the top-minus-bottom difference is not above 0; - fewer than 30 cases in total.
