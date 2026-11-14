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
- Situation: sharp up move on unusually low volume -> adapted: a veto selects up bars whose volume is at most 70% of the 20-bar average, and inside that regime the position grows with the size of the bar's rise.
- Comparison: volume against its usual level -> kept: volume is compared with its own 20-bar average.
- Outcome: price falls back after the rise -> adapted: "followed by" becomes a short held through the next bar, while the situation is present.
- Verdict transfer: yes: a short sized by the move, taken only on thin-volume up bars, gains exactly when those rises are partly given back.
Forecast: A veto checks each bar with `VolumeExpansionHedgeComponent` (vol_period 20, sf 20). That component reads -(1 - volume/average) x 20 on up bars with below-average volume. When its value is at or below -6 (volume at most 70% of its average), the bar goes to `mean_reversion`. Every other bar is flat. In `mean_reversion`, the forecast is the one-bar percent rise (`PriceEvolutionComponent`, period 1). It is standardised against its own last 60 values, so an average-size daily move is about 10. It is then negated, put through `signed_power` with exponent 3 (pivot 10) and clipped to at most 0. The result is always zero or negative: about -1.25 for a half-average rise, -10 for an average rise, and -20 at the cap for rises of about 1.26 times average or more. It is zero on every bar that is not a thin-volume up bar.
Config: 003-01_low-volume-up-move-reverts_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The coin's next-bar return after each bar with a non-zero forecast, minus the coin's mean one-bar return over all bars of the windows. One value per case; cases do not overlap.
- Supporting check: Across those cases, the correlation between |forecast| and the strategy's next-bar gain should be positive.
- Confirm: The mean excess next-bar return is negative with t <= -2.0, pooled over all windows.
- Reject: The mean excess next-bar return is positive with t >= +2.0, meaning thin-volume rises carry on.
- Inconclusive: A t between -2.0 and +2.0 is inconclusive, as is any result from fewer than 30 active cases.
