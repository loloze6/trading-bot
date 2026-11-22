---
idea: 024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound
brief: 024_exhaustion-after-an-extended-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 9111077ea370
---
Fidelity:
- Situation: a coin has just fallen in an unbroken streak of 4h bars, on declining volume -> adapted: "just after the streak" becomes "while the streak is running" (a regime on the volume slope across the streak being negative).
- Comparison: the streak's loss against the coin's typical 4h move over the past 30 days -> kept: the loss divided by the mean absolute one-bar return over 180 bars.
- Outcome: it rises over the next three days, more the larger the scaled loss -> kept: long, sized by the scaled loss, held 18 bars.
- Verdict transfer: yes: the config measures the streak, the fading volume, the scaled loss and the 3-day rise as stated.
Forecast: The regime is active only while the current down-streak has volume falling across it, meaning the `DownStreakVolumeFadeComponent` slope is above 0 (side "down", statistic "slope"). In that regime the forecast is the streak's summed loss in usual one-bar moves from `DownStreakLossInUsualMovesComponent` (window 180, max_bars 180, side "down", base "start"), standardised over 180 bars with min_periods 45. The forecast is positive and grows linearly with the scaled loss. It is 0 when bar t did not close down, when volume did not fade, or outside the regime. It is never negative (long only).
Config: 024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: The unusual move per case. A case is a bet (a forecast rise of at least 2 points), read once per 18-bar grid cell. Its unusual move is the coin's 18-bar return from the signal bar's close minus the coin's normal 18-bar drift (holding the coin). The measure is the mean over the cases, pooled over coins and windows, with its t.
- Supporting check: Cases whose forecast is above the median case forecast have a larger mean unusual move than cases below it (difference above minus below > 0).
- Confirm: The mean unusual move is > 0 with t >= 2, and the supporting check's difference is > 0.
- Reject: The mean unusual move is < 0 with t <= -2.
- Inconclusive: Any t between -2 and 2, or t >= 2 with the size check not passing, or fewer than 30 cases in total.
