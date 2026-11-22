---
idea: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size
brief: 024_exhaustion-after-an-extended-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: aaeaf3675030
---
Fidelity:
- Situation: the coin has just risen in an unbroken streak of 4h bars -> adapted: "just after the streak" becomes "while the streak lasts"; the reading is positive on each bar of an up-streak and 0 once a bar closes down or flat.
- Comparison: the streak's gain relative to the typical 4h move over the past 30 days -> kept: the streak's gain divided by the mean absolute one-bar return over 180 bars, graded.
- Outcome: the coin keeps rising over the next three days, more so after larger streaks -> kept: the long position is held 18 bars and grows with the scaled gain.
- Verdict transfer: yes: the forecast is the idea's own scaled streak gain and the bet is held for its three days, so the test's result is the idea's result.
Forecast: The forecast uses DownStreakLossInUsualMovesComponent with side "up", window 180 (30 days of 4h bars), max_bars 180 and base "start". Its value is the summed gain of the current unbroken up-streak, as a fraction of the streak's starting close, divided by the coin's mean absolute 4h return over the last 180 bars. It is standardised against its own past 181 values (min_periods 45). The forecast is positive while an up-streak lasts and grows with the streak's gain counted in usual moves. It is 0 on any bar that closes down or flat, and it is never negative. Each rise of the forecast is held for 18 bars.
Config: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: The sample is the non-overlapping 18-bar grid of each window, using grid bars where the forecast is above 0. For each such bar, take forecast/10 × (the coin's 18-bar return − its normal 18-bar drift over all windows). The measure is the t of the mean of these values, before costs.
- Supporting check: On the same cases, split at the median forecast. Take the excess 18-bar return of the top half minus that of the bottom half (Welch t). This difference must be above 0 with t ≥ 1.
- Confirm: The main measure's t is ≥ 2 and the supporting check passes.
- Reject: The main measure's t is ≤ -2: forecast-weighted excess returns after up-streaks are reliably negative, so the streaks reverse.
- Inconclusive: Also inconclusive: - a main t between -2 and 2; - a main t ≥ 2 while the supporting check fails; - fewer than 100 grid cases with a forecast above 0 across all coins and windows.
