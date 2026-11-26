---
idea: 069-02_below-high-up-day-fade
brief: 069_low-in-range-rise-fades
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 503ce793b4fe
---
Fidelity:
- Situation: a coin closes up on the day -> kept: a regime rule on the one-day return above 0; the book holds nothing on other days.
- Comparison: how far the close sits below its 20-day high, in units of its 20-day daily swing -> kept: VolatilityScaledDistanceFromHighComponent (20-day high of highs, bar t included, over the std of 20 daily returns).
- Outcome: the price falls over the next day, more so the deeper the close -> kept: a short graded by that depth, held 1 bar.
- Verdict transfer: yes: the test measures the idea's own condition, depth measure and next-day outcome.
Forecast: On up days only (close above the previous close), the forecast is the close's distance below the highest high of the last 20 days, bar t included, divided by that high and by the std of the last 20 daily returns. The value is standardised over its past 60 values. It is never positive: 0 when the up day closes at the 20-day high, and it grows more negative (a larger short) the deeper the close sits below that high in usual daily moves. On average it is about -10 and it is capped at -20. On every other day the forecast is 0.
Config: 069-02_below-high-up-day-fade_1d_config.json
Side: short only (the brief): each component's forecast capped at 0 by step 3's code
Criterion:
- Horizon: 1 bar
- Main measure: On up-day bars (regime mean_reversion), the gain is (forecast / 10) x (the next day's return minus the coin's mean daily return over all its windows). The measure is the mean of that gain, with its t, taking the cases of one day across coins together.
- Supporting check: The mean excess next-day return of the deepest third of up days (most negative forecast) minus that of the shallowest third must be below 0.
- Confirm: The idea is confirmed when the mean gain is positive with t >= 2 and the supporting check passes.
- Reject: The idea is rejected when the mean gain is negative with t <= -2: deeper up-day closes are followed by stronger next-day moves.
- Inconclusive: Any t between -2 and 2 is inconclusive, and so is t >= 2 with a failed check. The test needs at least 300 up-day cases on at least 300 distinct days; with fewer it is also inconclusive.
