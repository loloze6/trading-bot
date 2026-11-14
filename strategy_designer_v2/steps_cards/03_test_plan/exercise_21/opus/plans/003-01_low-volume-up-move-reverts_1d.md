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
- Situation: sharp up move on unusually low volume -> adapted: an up bar with volume below its 20-bar average opens a regime, and the 1-bar rise sizes the position through a graded dead zone.
- Comparison: volume against its usual level -> kept: the bar's volume is compared with its 20-bar mean through VolumeExpansionHedgeComponent in a veto.
- Outcome: price falls back, giving up part of the rise -> adapted: "after the move" becomes a short held over the next bar, and the multi-bar holding period is dropped.
- Verdict transfer: yes: a short sized by the move, active only on low-volume up bars, gains exactly when those moves revert.
Forecast: On daily bars, the detector reads VolumeExpansionHedgeComponent (vol_period 20). That value is below 0 only on an up bar whose volume is under its 20-bar average. A veto on that value selects `mean_reversion`, and every other bar is `unknown`, which is flat. In `mean_reversion`, the forecast is the 1-bar percent move (PriceEvolutionComponent, period 1). It is standardised against its last 60 values, negated, and passed through signed_power with exponent 2 (pivot 10) as a graded dead zone, then clipped at max 0. The forecast is therefore zero outside low-volume up bars and never positive. On a qualifying bar it is short, small after an ordinary rise and growing with the square of the rise's size relative to recent daily moves. The combined forecast is capped at -20.
Config: 003-01_low-volume-up-move-reverts_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Take each bar with a non-zero forecast and multiply its |forecast| by the coin's next-bar return minus the coin's mean daily return over the same windows (the hold baseline). Compute the t-statistic of the mean of these weighted excess returns. The 1-bar returns do not overlap, so each case counts once.
- Supporting check: Split active bars into the top and bottom halves by |forecast|. The top half should show a lower mean excess next-bar return than the bottom half.
- Confirm: The weighted mean excess next-bar return is negative with t ≤ -2, pooled across the 6 windows. Equivalently, the short's pre-cost gain beats holding with t ≥ 2.
- Reject: The weighted mean excess next-bar return is positive with t ≥ +2. That would mean thin-volume rises carry on rather than revert.
- Inconclusive: Any t between -2 and +2 is inconclusive, including an estimate near zero. Fewer than 30 active bars pooled across the windows is also inconclusive.
