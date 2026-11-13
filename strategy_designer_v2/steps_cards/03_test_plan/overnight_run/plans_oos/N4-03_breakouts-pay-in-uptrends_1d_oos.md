---
idea: N4-03_breakouts-pay-in-uptrends
brief: 002_moving-average-cross-trend-persistence
data-instruments: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ
data-bar: 1d
data-period: folds A, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a new 20-day closing high -> adapted: the on/off new-high event becomes a graded position of the close in its 20-day close range, with a cubic dead zone so only closes at or near the top count.
- Comparison: close above versus below its own 200-day mean -> kept: a regime rule on the close's percent distance from its 200-day SMA, split at zero.
- Outcome: a rise after the high above the average, a fall over the next ten days below it -> adapted: "after the high" becomes "while at the high"; the ten-day hold is dropped and used as the horizon.
- Verdict transfer: yes: with the high, the condition and the direction all in place, a confirm or reject of this graded test is a confirm or reject of the idea.
Forecast: The regime detector reads the close's percent distance from its 200-day SMA. At zero or above, the bar is `trending`. Below zero, it is `mean_reversion`. In both regimes, the forecast starts from the 20-day Donchian range position of the close. This is +20 when the close is the highest close of the last 20 days and -20 at the lowest. It is standardised (window 60, min_periods 20) and clipped at 0, so only the upper half of the range counts. Then `signed_power` with exponent 3 and pivot 20 is applied: a close at the top stays near +20, and a value of 10 shrinks to 2.5. Mid-range bars and bars in the lower half give 0. In `trending` that value is the forecast: long, and largest at new highs. In `mean_reversion` it is negated: short, and largest at new highs. The `unknown` regime, used only before the SMA exists, is flat. The size grows smoothly as the close approaches its 20-day high.
Config: N4-03_breakouts-pay-in-uptrends_1d_oos_config.json
Criterion:
- Horizon: 10 bars
- Main measure: On bars where |forecast| >= 10, take sign(forecast) x (10-bar forward return - holding). Holding is the coin's mean 10-bar return over all windows pooled. Use one case per non-overlapping 10-bar block per coin, and pool across coins.
- Supporting check: Compute the same measure separately for `trending` bars (forward excess return) and `mean_reversion` bars (negative forward excess return). Report each side's sign and t.
- Confirm: The pooled mean signed excess return is > 0 with t >= 2 on non-overlapping cases.
- Reject: The pooled mean signed excess return is < 0 with t <= -2 on non-overlapping cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a pool with fewer than 30 non-overlapping cases, or fewer than 10 in either regime.
