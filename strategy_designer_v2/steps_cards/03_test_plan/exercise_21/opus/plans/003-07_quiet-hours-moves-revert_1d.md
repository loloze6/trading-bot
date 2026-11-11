---
idea: 003-07_quiet-hours-moves-revert
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a sharp move while volume is low (quiet hours, weekends) -> adapted: a daily move on a day whose volume is below its 20-day mean, sized by the move; intraday hours are not visible on 1d bars.
- Comparison: partial reversal against no reversal -> kept: the sign of the next return relative to the move.
- Outcome: price moves back against the thin-volume move once volume returns -> adapted: "once volume returns" becomes the next bar's return after the low-volume close.
- Verdict transfer: yes: low volume is the idea's operative condition, and a low-volume weekend day is a daily bar, so a daily confirm or reject bears on the idea.
Forecast: The forecast is active only on bars whose volume is below its 20-bar mean. A veto on volume puts those bars in the mean_reversion regime; every other bar is flat. On active bars the forecast is the 1-day percent price change, standardised against its own last 60 values and negated. That makes it contrarian: short after an up day, long after a down day. Signed_power with exponent 3 is then applied, so ordinary days give a position near zero and only sharp moves build a large one, capped at ±20. The forecast is zero when the day did not move or when volume is at or above its average.
Config: 003-07_quiet-hours-moves-revert_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On active bars, position × (next-bar return minus that window's mean daily return), so the coin's own drift is not credited. Its t-statistic is pooled over the 6 windows, before costs.
- Supporting check: On the active bars with the 20 percent largest |forecast|, the share where the next-bar return has the sign of the position.
- Confirm: Mean drift-adjusted position-weighted next-bar return above 0 with t ≥ 2.
- Reject: Mean below 0 with t ≤ -2, meaning low-volume sharp moves continue.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a test with fewer than 150 active bars, or fewer than 30 bars with |forecast| ≥ 10.
