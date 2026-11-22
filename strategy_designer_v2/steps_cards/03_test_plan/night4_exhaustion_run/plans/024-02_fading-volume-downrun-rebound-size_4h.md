---
idea: 024-02_fading-volume-downrun-rebound-size
brief: 024_exhaustion-after-an-extended-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: aaeaf3675030
---
Fidelity:
- Situation: the coin has just fallen in an unbroken streak of 4h bars with declining volume across the streak -> adapted: "after X" becomes "while X". A regime is active while the current down-streak's volume slope (DownStreakVolumeFade) is above 0.
- Comparison: the streak's loss against the coin's typical 4h move over the past 30 days -> kept: the streak loss is divided by the mean absolute one-bar return over 180 bars.
- Outcome: the coin rises over the next three days, more for a larger relative loss -> kept: long, sized by the relative loss, held 18 bars.
- Verdict transfer: yes: the test measures the idea's own streak, volume fade, loss scale and 3-day rise.
Forecast: The regime turns on while the current 4h down-streak has at least 2 bars and its volume is fading. This uses DownStreakVolumeFadeComponent, side "down", statistic "slope", with a value above 0. In that regime the forecast is long. Its size is the streak's summed loss divided by the mean absolute 4h return of the last 180 bars (30 days), from DownStreakLossInUsualMovesComponent. That value is standardised against its own past 180 values, so an average reading gives about +10, capped at 20. The forecast grows linearly with the loss in usual moves. It is zero when there is no down-streak or when volume is not fading. It is never negative.
Config: 024-02_fading-volume-downrun-rebound-size_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: For each case, take the coin's 18-bar return from the signal bar's close minus the coin's normal 18-bar drift over all its windows. A case is a long bet, a forecast rise of at least 2, read once per 18-bar grid cell. Pool the cases over coins and windows and take the mean and its t.
- Supporting check: The cases with an above-median forecast must have a larger mean unusual move than the cases below the median (difference above 0).
- Confirm: Mean unusual move above 0 with t ≥ 2 over at least 30 cases, and the supporting check passes.
- Reject: Mean unusual move below 0 with t ≤ -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2, a confirming t whose supporting check fails, or fewer than 30 cases.
