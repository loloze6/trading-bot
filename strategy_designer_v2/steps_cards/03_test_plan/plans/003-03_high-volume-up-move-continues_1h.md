---
idea: 003-03_high-volume-up-move-continues
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: sharp up move on unusually high volume -> adapted: an up bar with volume at or above its 20-bar mean opens the regime, and the position grows with the size of the move; the volume threshold is the only one the `volume_filter` veto allows.
- Comparison: against the coin's normal drift (holding it) -> kept
- Outcome: price keeps rising afterwards -> adapted: "after the move" becomes "on the bar after the move", and the holding period is dropped.
- Verdict transfer: yes: the forecast is long only after high-volume up bars and larger after sharper ones, so continuation beyond holding the coin confirms the idea and its absence rejects it.
Forecast: A regime veto watches the one-bar price change (`PriceEvolutionComponent`, period 1). Its `volume_filter` (period 20) sets that change to 0 unless the bar's volume is at or above its 20-bar mean. The veto fires when the filtered change is above 0, which means an up bar on above-average volume, and it selects `trending`. On every other bar the forecast is 0 (flat). In `trending`, the forecast is the same one-bar change, standardised against its own past 60 values and clipped at 0. It is positive and grows with the size of the move: an average move gives about +10, a move twice the average gives the cap of 20. It is never negative.
Config: 003-03_high-volume-up-move-continues_1h_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The position-weighted mean of the next-bar close-to-close return over the active bars, minus the coin's unconditional mean one-bar return in the same window. Measured before costs and pooled over the 6 windows; each active bar is one case.
- Supporting check: For the top fifth of positions (the sharpest high-volume up bars), the mean next-bar return minus the unconditional mean.
- Confirm: The pooled excess is above 0 with a t-stat of at least 2, it is positive in at least 4 of the 6 windows, and the top-fifth excess is also positive.
- Reject: The pooled excess is at or below 0, or the top-fifth excess is negative with a t-stat of -2 or below (high-volume moves revert).
- Inconclusive: A positive excess with a t-stat below 2, or one positive in fewer than 4 windows, decides nothing. So does any result with fewer than 300 active bars in total or fewer than 60 in the top fifth.
