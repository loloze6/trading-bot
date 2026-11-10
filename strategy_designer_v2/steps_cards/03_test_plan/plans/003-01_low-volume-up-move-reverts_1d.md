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
- Situation: a sharp up move on unusually low volume -> adapted: an up daily bar with volume below its 20-bar average is an on/off regime condition, and the size of the move grades the position.
- Comparison: volume judged against its usual level -> adapted: "unusually low" becomes "below the 20-bar mean volume, current bar included".
- Outcome: price falls back, giving up part of the rise -> adapted: "after X" becomes "while X", so the short is held over the next bar and no holding period is kept.
- Verdict transfer: yes: a next-day giveback after thin up days, sized by the move, is the idea's claim on daily bars.
Forecast: The regime detector reads VolumeExpansionHedgeComponent (vol_period 20). It is below 0 only on an up bar whose volume is below its 20-bar average. A veto sends exactly those bars to `mean_reversion`, and every other bar is `unknown`, which is flat. In `mean_reversion` the forecast is the one-bar percent move (PriceEvolutionComponent, period 1), standardised over its last 60 values, negated, and clipped at 0 from above. The result is short only. Its size grows with how large today's rise is against recent absolute daily moves: an average move gives about -10, and the cap is -20. It is zero on every other bar.
Config: 003-01_low-volume-up-move-reverts_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The coin's next-bar return after each thin-volume up bar, weighted by the position. It is taken minus the coin's unconditional mean next-bar return in the same window, so the market's drift is not credited to the idea. All 6 windows are pooled, and each case is counted once (1-bar horizon, no overlap).
- Supporting check: Split the cases into thirds by |position|. The largest third should show a larger mean next-bar drop, measured against the unconditional mean, than the smallest third.
- Confirm: The drift-adjusted, position-weighted next-bar return of the short is above 0 with a t-stat of at least 2.0. The largest third also reverts more than the smallest third.
- Reject: The drift-adjusted next-bar return after thin up bars is at or above the coin's unconditional mean, meaning the short earns 0 or less after the drift adjustment, with a t-stat of 0 or below.
- Inconclusive: A positive drift-adjusted result with a t-stat between 0 and 2, or a confirmed mean without the size ordering. Fewer than 60 qualifying bars across all windows is also inconclusive.
