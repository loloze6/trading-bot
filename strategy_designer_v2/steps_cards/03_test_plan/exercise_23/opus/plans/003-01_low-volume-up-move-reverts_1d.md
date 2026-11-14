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
- Situation: a sharp upward move on unusually low volume -> adapted: the 1-bar rise is graded and damped when small; "unusually low volume" becomes the on/off condition "volume below its 20-bar mean".
- Comparison: none (the idea is judged against the coin's own drift) -> kept
- Outcome: price then falls back, giving up part of the rise -> adapted: measured as the next bar's return being negative while short, with no holding period.
- Verdict transfer: yes: the test shorts sharp low-volume up-days in proportion to their size and checks whether the next day falls, which is the idea itself.
Forecast: The regime detector checks one condition on each daily bar: is today's volume below its 20-bar mean (a veto using `volume_filter` on a constant)? If yes, the bar is `mean_reversion`. If no, the bar is flat (forecast 0). In `mean_reversion`, the component is today's 1-bar percent change in close. It is standardised against the mean absolute size of the 60 previous daily moves, then sign-flipped, then clipped at a maximum of 0, so only up-days give a position, and that position is short. Last comes `signed_power` with exponent 3. A typical-size rise gives about -10. Small rises are pushed close to 0, for example half a typical rise gives -1.25. Large rises grow quickly, up to the -20 cap. Down-days and high-volume days give 0. The forecast is never positive.
Config: 003-01_low-volume-up-move-reverts_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The coin's next-bar return on bars where the forecast is -5 or below, minus the coin's average next-bar return over all bars in the same windows. Each bar is counted once, and the 6 windows are pooled.
- Supporting check: Across all bars where the forecast is below 0, the rank correlation between |forecast| and the next-bar return should be negative.
- Confirm: The excess next-bar return after strong signals is negative with t ≤ -2, and the supporting check is negative.
- Reject: The excess next-bar return after strong signals is positive with t ≥ +2, meaning low-volume rises keep going.
- Inconclusive: Any t between -2 and +2, including estimates near zero. The result is also inconclusive if there are fewer than 30 bars with a forecast of -5 or below across the 6 windows.
