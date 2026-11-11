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
- Situation: a sharp upward move made on unusually low volume -> adapted: "unusually low volume" becomes an on/off regime (an up bar with volume below its 24-bar average), and "sharp" is graded by the size of the day's rise.
- Comparison: none -> kept
- Outcome: price then falls back, giving up part of the rise -> adapted: holding period dropped; the short is held only on the bar after each thin-volume up day.
- Verdict transfer: yes: thin-volume up days and their rise size are measured as stated, so the sign and strength of the next bar's fall bear directly on the idea.
Forecast: The regime turns on only on an up day whose volume is below its 24-day average. That measure is VolumeExpansionHedgeComponent below 0 in the detector. On those days the forecast is short, sized by the day's percent rise: PriceEvolutionComponent with period 1, standardised over its past 60 values and negated. A signed_power with exponent 3 and pivot 20 then shrinks ordinary rises to near zero, so only sharp rises get a large short. On every other bar the forecast is zero. It never goes long.
Config: 003-01_low-volume-up-move-reverts_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On each bar with a non-zero forecast, take allocation × (the next bar's return minus the coin's mean daily return in that window). Pool these across all 6 windows and compute the t-statistic of their mean, before costs. Horizons are one bar, so nothing overlaps.
- Supporting check: The next-bar return after the largest third of short positions is below the return after the smallest third.
- Confirm: The mean position-weighted excess return is positive with t ≥ 2, meaning the next bar falls relative to holding the coin.
- Reject: The mean is negative with t ≤ -2, meaning thin-volume rises go on to beat holding the coin.
- Inconclusive: Any t between -2 and 2, including results near zero. Also any run with fewer than 30 active bars (non-zero forecast) pooled across the windows.
