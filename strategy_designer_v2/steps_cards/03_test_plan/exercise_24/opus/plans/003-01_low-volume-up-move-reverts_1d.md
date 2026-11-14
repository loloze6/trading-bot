---
idea: 003-01_low-volume-up-move-reverts
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a sharp upward move on unusually low volume -> adapted: the one-bar rise made graded by its size, and kept only on up bars whose volume is below its 20-bar average.
- Comparison: volume judged against its usual level -> kept: the bar's volume is compared with its 20-bar average volume.
- Outcome: price falls back, giving up part of the rise -> adapted: the holding period is dropped, so this is the next bar's return, expected negative.
- Verdict transfer: yes: a short sized by the thin-volume rise earns exactly when price gives back part of the rise on the next bar.
Forecast: The regime detector reads `VolumeExpansionHedgeComponent` with `vol_period` 20, which is negative only on up bars whose volume is below its 20-bar average. When that value is below 0, the bar becomes `mean_reversion`. Every other bar is flat. In `mean_reversion` the forecast is the current bar's one-bar return (`PriceEvolutionComponent`, `period` 1), standardised over its past 60 values and negated. It then goes through `signed_power` with exponent 3 as the dead zone and is clipped at 0 or below. So the forecast is zero or negative, a short only. It is near 0 for a small rise and grows steeply with the size of the thin-volume rise, up to the cap of -20.
Config: 003-01_low-volume-up-move-reverts_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Take each bar where the forecast is below 0. Compare the coin's next-bar return there with the coin's mean next-bar return over all bars of the windows (the buy-and-hold baseline). Report the difference and its t-statistic, pooled over the 6 windows.
- Supporting check: Across those bars, the slope of the next-bar return on the forecast should be positive: larger shorts should be followed by larger falls.
- Confirm: The next-bar return on event bars is below the all-bar mean, with t ≤ -2.
- Reject: The next-bar return on event bars is above the all-bar mean, with t ≥ +2.
- Inconclusive: Any t between -2 and +2, or fewer than 30 event bars that traded (|forecast| ≥ 2) across all windows.
