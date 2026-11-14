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
- Situation: a sharp upward move on unusually low volume -> adapted: the one-bar rise is graded by its size; "low volume" is kept as a regime rule (an up bar with volume below its 20-bar average).
- Comparison: none -> kept
- Outcome: price falls back, giving up part of the rise -> adapted: "after the move" becomes "while on the move's bar", and the holding period is dropped, so the short is held one bar.
- Verdict transfer: yes: a short sized by the rise, taken only on low-volume up bars, gains if and only if those rises are partly given back.
Forecast: The regime detector reads VolumeExpansionHedgeComponent (vol_period 20). It is below 0 only on an up bar whose volume is below its 20-bar average, and that bar is labelled mean_reversion. Every other bar is unknown and flat. In mean_reversion, the forecast is the one-bar percent rise (PriceEvolutionComponent, period 1). It is standardised against its last 60 values, negated, then passed through signed_power with exponent 3 as the strongest graded dead zone. The forecast is therefore negative (short) only on low-volume up bars and zero elsewhere. A small rise gives a tiny short; a sharp rise gives a short growing with the cube of its size, capped at -20.
Config: 003-01_low-volume-up-move-reverts_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On each active bar, take the position (forecast/10) times the coin's next-bar return minus the coin's mean daily return over the same window, pooled across the 6 windows. Report the mean and its t-statistic. Each bar is counted once, since the horizon is 1 bar and nothing overlaps.
- Supporting check: The mean next-bar return after the top third of positions by size should be more negative than after the bottom third.
- Confirm: The mean excess return of the position is positive with t ≥ 2.
- Reject: The mean excess return of the position is negative with t ≤ -2, meaning low-volume rises carry on beyond the coin's drift.
- Inconclusive: Any t between -2 and 2, or fewer than 30 active bars across all windows. Note: the key "mean_reversion_unused" in the config above is an error; read the strategies block as: {"regimes":{"mean_reversion":{...as above...},"trending":null,"unknown":null,"chop":null}}
