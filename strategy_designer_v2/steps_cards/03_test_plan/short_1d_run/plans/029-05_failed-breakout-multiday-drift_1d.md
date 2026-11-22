---
idea: 029-05_failed-breakout-multiday-drift
brief: 029_failed-breakout-traps-late-buyers
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 02605c0f0d60
---
Fidelity:
- Situation: a close back below the old 20-day high within 3 days of a close above it -> adapted: "after the failure" becomes "while" the failure reading is non-zero (FailedBreakoutDepthComponent, breakout 1 to 3 bars before the close, source close, delayed 2 bars).
- Comparison: the deeper the re-entry close sits below the old high -> kept: the depth of that close below the old high, in percent of the high, sizes the short.
- Outcome: the fall from day 2 to day 10 after the failure -> kept: entry 2 bars after the failure close (lag 2), held 8 bars, short.
- Verdict transfer: yes: the test bets short, sized by the re-entry depth, exactly over days 2 to 10 after the failure.
Forecast: One component, FailedBreakoutDepthComponent (period 20, fail_window 3, source close, reference prior_high, exclude_current 1, lag 2). At bar t it reads the failure bar e = t-2. It looks for a close above the prior 20 closes on one of bars e-3 to e-1. If bar e's close sits back below that old high, the reading is the depth of that close below the high, in percent. Otherwise it is 0. The reading is standardised over its last 60 values and then negated. The forecast is therefore 0 on every bar without a recent failure, and negative (short only) from day 2 after a failure. Its size grows with how deep the re-entry close sat below the old high, up to the cap of -20.
Config: 029-05_failed-breakout-multiday-drift_1d_config.json
Criterion:
- Horizon: 8 bars
- Main measure: Each case is a short bet (a fall of the forecast of at least 2 points), read once per 8-bar grid cell. For each case, take the coin's 8-bar return from the signal bar's close, minus the coin's normal 8-bar drift over all windows, signed for the short side. Measure the mean of this unusual move and its t, before costs.
- Supporting check: Split the cases at the median of the entry forecast's size. The mean short-side unusual move of the deeper half, minus that of the shallower half, must be above 0.
- Confirm: The main measure's mean is positive with t >= 2, and the supporting check passes (deeper minus shallower above 0).
- Reject: The main measure's mean is negative with t <= -2: prices rise more than their drift from day 2 to day 10 after failures.
- Inconclusive: These results neither confirm nor reject: a t between -2 and 2; or t >= 2 with the deeper half not beating the shallower half; or fewer than 30 independent cases over all coins and windows.
