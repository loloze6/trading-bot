---
idea: 031-02_down-streak-length-reversal
brief: 031_daily-close-streak-reversal-or-continuation
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 31f1a8c6c7f6
---
Fidelity:
- Situation: a coin has closed lower several days in a row (the down-close streak length) -> kept: MovingAverageAgeComponent with SMA period 2 counts consecutive closes below the prior close, clipped to down streaks only.
- Comparison: against its own down-close streak lengths over the past 365 days -> kept: the down-streak count is scaled by the mean of its own down-streak counts over the prior 365 daily bars.
- Outcome: the longer the streak, the more it rises over the next 5 days -> kept: a long position graded by relative streak length, held 5 daily bars.
- Verdict transfer: yes: a forecast that grows with the coin's relative down-streak length, scored against 5-day forward returns, confirms or rejects exactly this claim.
Forecast: The component is MovingAverageAgeComponent with period 2 and max_bars 120. A close below its 2-bar SMA is a close below the previous close, so the component reads -n after n down closes in a row. The history transform keeps only the down side (clip max 0), so the history holds 0 on up-close bars and -n during a down streak. `standardise` (window 365, min_periods 91) divides today's value by the mean absolute down-streak count over the prior 365 days, times 10. `negate` then makes it positive. The forecast is 0 when the last close was up. It is positive during a down streak and grows with each further down close, larger the longer the streak is against the coin's usual down streaks. It is capped at 20 and never goes below 0.
Config: 031-02_down-streak-length-reversal_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: This is measured on the non-overlapping 5-bar grid of each window, pooling all coins. On each grid bar, take the coin's 5-bar forward return minus its mean 5-bar return over all windows. Regress that excess return on the recorded forecast and read the slope's t, with same-day cases summed per day.
- Supporting check: The mean unusual move over the cases (forecast rises of at least 2 on the grid, in the long direction) is above 0.
- Confirm: The slope is positive with t >= 2, and the supporting check passes.
- Reject: The slope is negative with t <= -2.
- Inconclusive: Any slope with t between -2 and 2 is inconclusive. So is a confirming slope whose supporting check fails. The test needs at least 300 grid bars with a forecast above 0, on at least 100 distinct days; fewer is inconclusive.
