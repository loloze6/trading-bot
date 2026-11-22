---
idea: 024-02_fading-volume-downrun-rebound-size.b2_extreme-down-streak-rebound-any-volume
brief: 024_exhaustion-after-an-extended-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: aaeaf3675030
---
Fidelity:
- Situation: a coin has just fallen in an unbroken streak of 4h bars -> adapted: "just fallen" becomes "while the down-streak lasts", the current streak's loss read on each bar.
- Comparison: the streak's loss against several times its typical 4h move over the past 30 days -> adapted: the loss is measured in mean absolute 4h moves over 180 bars, and "several times" becomes a graded strength.
- Outcome: it rises over the next one to three days, more after larger losses -> kept: long, held 18 bars (three days), size growing with the loss.
- Verdict transfer: yes: the component measures exactly the streak's loss in usual 4h moves over 30 days, volume is ignored as the idea says, and the rebound is tested over the stated horizon.
Forecast: One component, DownStreakLossInUsualMovesComponent (window 180 bars = 30 days, side "down", base "start"). It gives the summed loss of the current unbroken streak of down closes, divided by the mean absolute 4h return of the last 180 bars. It is 0 on any bar that did not close down. It is standardised against its own past 180 values (min_periods 45). Then signed_power with exponent 3 and pivot 20, the strongest graded dead zone allowed, keeps short or mild streaks near 0 and amplifies extreme ones. The forecast is never negative, so it is long only. It is 0 when there is no down-streak, small for ordinary streaks, and grows steeply as the streak's loss reaches several usual moves.
Config: 024-02_fading-volume-downrun-rebound-size.b2_extreme-down-streak-rebound-any-volume_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: Take each case (a rise of the forecast of at least 2 points, read once per cell of the 18-bar grid of each window). For each case, take the coin's 18-bar return from the signal bar's close minus the coin's normal 18-bar drift over all windows. Measure the t of the mean of these unusual moves.
- Supporting check: Split the cases at the median forecast of the cases. The mean unusual move of the cases above the median, minus that of the cases below it, is above 0.
- Confirm: The mean unusual move is positive with t >= 2 over at least 30 cases, and the supporting check passes.
- Reject: The mean unusual move is negative with t <= -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2, or a positive t >= 2 where the supporting check fails, or fewer than 30 cases in total.
