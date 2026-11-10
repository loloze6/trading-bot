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
- Situation: sharp up move on unusually low volume -> adapted: an up day with volume below its 20-day average starts a regime; inside it, the position grows with the size of the day's rise.
- Comparison: low volume versus the coin's usual volume -> adapted: "unusually low" is measured as volume below its own 20-bar mean, which includes the current day.
- Outcome: price falls back after the up move -> adapted: "after X" becomes "while X", so the short is held for the next bar only.
- Verdict transfer: yes: a short sized by the low-volume rise gains only if the price falls back after such rises.
Forecast: The forecast is negative only on a day that closes up on volume below its 20-day average (VolumeExpansionHedgeComponent below 0); every other day it is zero. On those days the size comes from that day's percent rise (PriceEvolutionComponent, period 1). The rise is standardised against its own last 60 values, then negated so the position is short. A signed_power with exponent 2 shrinks small rises toward zero and enlarges sharp ones, so a larger rise means a larger short, capped at -20.
Config: 003-01_low-volume-up-move-reverts_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Pool all 6 windows. On each bar with a non-zero forecast, compute allocation x (the coin's next-bar return minus that window's mean daily return), so the coin's own drift is removed. Report the mean and its t-statistic. Each case covers one bar, so no returns overlap.
- Supporting check: Across active bars, the slope of the next-bar excess return on the absolute forecast should be negative: sharper thin rises should be followed by larger drops.
- Confirm: The mean is above 0 with t ≥ 2 over at least 30 active bars.
- Reject: The mean is below 0 with t ≤ -2 over at least 30 active bars, meaning thin-volume rises carry on upward.
- Inconclusive: Any t between -2 and 2, or fewer than 30 active bars across the windows. With fewer than 30, report the result but draw no verdict.
