---
idea: 029-02_breakout-volume-trapped-decline
brief: 029_failed-breakout-traps-late-buyers
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 02605c0f0d60
---
Fidelity:
- Situation: a daily close above the prior 20-day high, followed within 3 days by a close back below that high -> adapted: "after the failure" made "while the close sits below the high it broke, 1 to 3 days after the breakout" (`FailedBreakoutVolumeRatioComponent`, period 20, source "high", fail_window 4).
- Comparison: the higher the breakout day's volume against its 20-day average, the larger the fall -> kept: the breakout bar's volume over its 20-bar mean volume sets the short's size.
- Outcome: the coin falls over the next 5 days -> kept: each short bet is held 5 daily bars and judged on the coin's 5-bar return.
- Verdict transfer: yes: the forecast is short exactly on failed-breakout bars, and its size follows the breakout volume ratio, so its 5-day outcome confirms or rejects the idea itself.
Forecast: The forecast uses one indicator, the failed-breakout volume ratio (prior 20-day high from the highs, breakout 1 to 3 days back, breakout-day volume over its 20-day mean). It is 0 on every bar except when the close is back below a high that was broken 1 to 3 days earlier. On those bars it is minus the ratio, so the position is short only. The ratio is put on the forecast scale by `standardise` (window 60, min_periods 20) with target 1, because the input is 0 on most bars. With the default target 10, every active bar would sit at the -20 cap. The short grows linearly with the breakout day's volume against its average. A `clip` with max 0 keeps the forecast from ever going above 0.
Config: 029-02_breakout-volume-trapped-decline_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are the short bets: a fall of the forecast of at least 2 points, read once per 5-bar grid cell of each window. For each case, take the coin's 5-bar return from the signal bar's close, minus the coin's normal 5-bar drift over all windows, counted in the short direction. The measure is the mean of this unusual move over all coins and windows, with the t of that mean.
- Supporting check: Regress each case's unusual short move on the size of its forecast at the bet (abs `post_pipeline_value` of `fb_vol`). The slope must be above 0: the higher the volume ratio, the larger the fall.
- Confirm: The idea is confirmed when the mean unusual short move is above 0 with t >= 2, and the supporting slope is above 0.
- Reject: The idea is rejected when the mean unusual short move is below 0 with t <= -2, that is, the coin rises more than its drift after failed breakouts.
- Inconclusive: Every result with t between -2 and 2 is inconclusive. So is a main t >= 2 with a slope at or below 0. Any result from fewer than 30 cases across all coins and windows is inconclusive.
