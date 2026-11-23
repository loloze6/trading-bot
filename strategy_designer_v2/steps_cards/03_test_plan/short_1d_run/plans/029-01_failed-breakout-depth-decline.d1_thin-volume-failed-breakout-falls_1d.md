---
idea: 029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls
brief: 029_failed-breakout-traps-late-buyers
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 5f0a6e1d2346
---
Fidelity:
- Situation: a close above the prior 20-day closing high, then within 3 days a close back below that old high -> adapted: "after the failure" becomes "while the close stays below the old high, up to 3 days after the breakout" (FailedBreakoutVolumeRatioComponent, period 20, fail_window 4).
- Comparison: breakout-day volume below its 20-day average, and the lower the volume the larger the fall -> kept: form "thin" gives max(0, 1 − volume[j] / 20-day mean volume), which is 0 on heavy-volume breakouts and grows as the volume thins.
- Outcome: the coin falls over the next 5 days -> kept: a short held for 5 daily bars, sized by thinness.
- Verdict transfer: yes: the forecast is short only on thin-volume failed breakouts and grows as the volume thins, so its 5-day results confirm or reject exactly this idea.
Forecast: The forecast uses one component, FailedBreakoutVolumeRatioComponent (period 20, fail_window 4, source close, volume_period 20, form "thin"). Its raw value is non-zero only on a bar whose close sits back below the prior 20-day closing high, when that high was broken by a close 1 to 3 days earlier. The value is then 1 minus the breakout day's volume over its 20-day mean, so it is 0 when that volume was at or above its average and grows toward 1 as it thins. It is standardised over 60 bars (min_periods 20), then negated. The forecast is therefore 0 on every other bar and negative (short) during a thin-volume failure. Its size grows with how thin the breakout volume was. It never goes above zero, because the brief is short only.
Config: 029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are short bets: the forecast falling by at least 2 points on its short side, taken once per non-overlapping 5-bar grid cell of each window. For each case, measure the coin's 5-bar return from the signal bar's close, minus the coin's normal 5-bar drift over all windows, in the short direction. Report the mean over all coins and cases, with its t.
- Supporting check: The graded claim. Split the cases at the median of abs(forecast) on the signal bar. The mean short-direction unusual move of the larger half minus that of the smaller half must be above 0.
- Confirm: The idea is confirmed only when both hold: the mean short-direction unusual move is above 0 with t ≥ 2, over at least 30 cases, and the supporting check difference is above 0.
- Reject: The mean short-direction unusual move is below 0 with t ≤ -2, over at least 30 cases: after thin-volume failures the coin rises more than its normal drift.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is a confirming main measure whose supporting check difference is 0 or below. Fewer than 30 cases is also inconclusive.
