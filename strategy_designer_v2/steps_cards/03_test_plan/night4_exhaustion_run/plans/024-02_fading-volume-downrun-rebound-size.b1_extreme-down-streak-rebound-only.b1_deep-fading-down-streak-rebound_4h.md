---
idea: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only.b1_deep-fading-down-streak-rebound
brief: 024_exhaustion-after-an-extended-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: aaeaf3675030
---
Fidelity:
- Situation: the coin has just fallen in an unbroken streak of 4h bars with volume declining across it -> adapted: the streak is read while it lasts at the bar's close ("after" made "while"), and "volume declining" is a regime rule on the streak's volume slope.
- Comparison: the streak's loss must be several times the coin's typical 4h move over 30 days, counted in that move and not against other streaks -> adapted: the loss is measured in the mean absolute 4h move over 180 bars, and "several times" is made graded with the strongest dead zone.
- Outcome: the price rises over the next three days, more when the loss is larger -> kept: a long held 18 bars, sized by the loss.
- Verdict transfer: yes: the streak, the fading volume, the loss in usual moves, the rise and its growth with the loss are all measured as the idea states them.
Forecast: The forecast is zero unless the coin's current bar closed down as part of a down-streak of at least two bars, and the volume slope across that streak is negative. That condition is the regime rule on `DownStreakVolumeFadeComponent` (raw value above 0). While the condition holds, the forecast is long and sized by the streak's loss. The loss is the cumulative fall of the streak divided by the mean absolute 4h return over the last 180 bars (30 days), from `DownStreakLossInUsualMovesComponent`. That value is standardised over its last 180 values. It then goes through `signed_power` with exponent 3 and pivot 20, the strongest graded dead zone allowed. A shallow streak (standardised 10) gives about 2.5, and only the deep ones approach 20. The forecast is never negative, and it falls to zero when the streak ends or the volume stops fading.
Config: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only.b1_deep-fading-down-streak-rebound_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: Each case is a bet, a rise of the forecast of at least 2 points, read once per 18-bar grid cell of each window. For each case, take the coin's 18-bar return from the signal bar's close minus the coin's normal 18-bar drift over all windows. The measure is the mean of these excess returns over all coins and cases, with its t-statistic.
- Supporting check: Across the cases, the correlation between the forecast at the signal bar and the 18-bar excess return must be positive.
- Confirm: The idea is confirmed when the mean excess return is positive with t ≥ 2 on at least 30 cases, and the supporting correlation is above 0.
- Reject: The idea is rejected when the mean excess return is negative with t ≤ -2 on at least 30 cases.
- Inconclusive: Any t between -2 and 2, or fewer than 30 cases, is inconclusive. A main measure with t ≥ 2 but a correlation of 0 or below is also inconclusive.
