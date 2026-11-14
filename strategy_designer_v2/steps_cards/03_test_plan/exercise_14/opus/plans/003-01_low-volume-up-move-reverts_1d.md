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
- Situation: a sharp upward move made on unusually low volume -> adapted: the volume part becomes an on/off regime condition. A veto fires on a daily up bar whose volume is below its 20-bar average, read from `VolumeExpansionHedgeComponent` in the detector, where on/off components are allowed. The sharpness part is graded: the size of that bar's rise (`PriceEvolutionComponent`, period 1), with a graded dead zone (`signed_power` 2) so small rises carry almost no position.
- Comparison: none in this idea. "Part of the rise" sets only the direction, and the brief's high-volume contrast belongs to a sibling idea -> kept
- Outcome: price falls back after the thin-volume rise (down) -> adapted: "after X" becomes "while X". The short is held only on the signal bar's close and judged on the next bar's return, so the multi-bar holding period is dropped.
- Verdict transfer: yes: if the drift-adjusted next-bar return after low-volume up bars is reliably negative, the idea is confirmed at its shortest horizon; if it is zero or positive, nothing falls back and the idea is rejected.
Forecast: On every daily bar the detector reads the volume-hedge value for the last 20 bars. - When the bar closed up on volume below its 20-bar average, a veto selects `mean_reversion`. On every other bar the regime is `unknown`, which is flat. - In `mean_reversion` the forecast is the bar's one-day percent change, standardised against its last 60 values (a typical absolute daily move gives 10, capped at 20). - That value goes through `signed_power` with exponent 2 and pivot 10. A small rise is damped towards 0, and a large one is amplified (15 becomes 22.5, final clip at 20). - It is then negated. Because the bar is an up bar, the forecast is always zero or negative: a short that grows with the size of the thin-volume rise. - It is zero on all bars outside the situation.
Config: 003-01_low-volume-up-move-reverts_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Pool all six windows. On every signal bar (forecast below 0), take the coin's next-bar close-to-close return. Measure its mean minus the mean next-bar return over all bars of the same windows. This is the drift-adjusted reversion, the edge over simply holding the coin, before costs. Each case is one non-overlapping 1-bar return, with a t-statistic on the signal-bar returns' excess.
- Supporting check: Split the signal bars into halves by the absolute size of the forecast. The larger-forecast half (sharper thin-volume rises) should show a more negative drift-adjusted next-bar return than the smaller half.
- Confirm: The drift-adjusted mean next-bar return on signal bars is negative with t ≤ -2.0. The strategy's cumulative return before costs is positive. The larger-forecast half is at least as negative as the smaller half.
- Reject: The drift-adjusted mean next-bar return on signal bars is zero or positive, which means thin-volume rises do not fall back relative to the coin's normal drift. Or the larger-forecast half is clearly less negative than the smaller half, with the overall t above -1.0.
- Inconclusive: The drift-adjusted mean is negative but with t between -2.0 and -1.0, or the supporting check contradicts the main measure. The result is also inconclusive if fewer than 60 signal bars occur across the six windows, whatever the result.
