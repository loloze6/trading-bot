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
- Situation: a sharp up move on unusually low volume -> adapted: an up day whose volume is below its 20-day average opens a regime (on/off), and the short is sized by the size of that day's rise.
- Comparison: none -> kept
- Outcome: price falls back, giving up part of the rise -> adapted: measured over the next day only, because the position lasts only while the situation holds.
- Verdict transfer: yes: a next-day fall after thin up days, graded by the size of the rise, is the idea's claim; its absence rejects it.
Forecast: A regime turns on when two things hold on the same day: the close is above the previous close, and the volume is below its 20-day average (VolumeExpansionHedgeComponent is below 0). On those days the forecast is short. Its size follows that day's rise: the 1-day percent change, standardised against its own past 60 values and negated. A larger rise gives a larger short, from near 0 for a tiny rise up to -20. On every other day the forecast is 0. It is never positive.
Config: 003-01_low-volume-up-move-reverts_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On thin-up days (regime active), the next-day return of BTC minus BTC's mean daily return over all window days. Each case counts once (no overlap), and all 6 windows are pooled.
- Supporting check: Across the active days, the slope of the next-day return on |forecast|, to check that larger thin rises give back more.
- Confirm: The mean excess next-day return after thin-up days is negative, with t ≤ -2.
- Reject: The mean excess next-day return after thin-up days is positive, with t ≥ +2.
- Inconclusive: Any t between -2 and +2, or fewer than 60 thin-up days pooled across the windows.
