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
- Situation: sharp one-day rise on unusually low volume -> adapted: low volume is a veto (volume below its 20-bar mean), and the size of the rise is graded.
- Comparison: volume against its usual level -> adapted: "unusually low" becomes "below its 20-bar average", the only volume threshold the detector offers.
- Outcome: price falls back after the rise -> adapted: short while the low-volume up bar is current; the holding period is dropped.
- Verdict transfer: yes: the test bets against exactly the low-volume up moves the idea names, sized by the move.
Forecast: Two parts decide each bar. First, a veto checks whether the daily bar's volume is below its 20-bar mean. Only then is the regime mean_reversion; on every other bar the forecast is flat. Second, in that regime the forecast is the bar's 1-day percent move, scaled by its mean absolute size over the 60 prior bars (target 10, cap 20). It is then negated and clipped to at most 0. The result is a short whose size grows with how sharp the low-volume up move is. Down bars and flat bars give 0.
Config: 003-01_low-volume-up-move-reverts_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The close-to-close return on the bar after each bar with a non-zero forecast. Compare it with the coin's mean 1-bar return over all tested bars, the buy-and-hold baseline. Pool the cases across the 6 windows; each case counts once.
- Supporting check: Over the same active bars, regress the next-bar return on the forecast. The slope should be positive (a bigger short comes before a bigger fall). Separately, the 3-bar forward return should also sit below the 3-bar baseline, with non-overlapping cases counted once.
- Confirm: The mean next-bar return after active bars is below the baseline mean. The difference has a one-sided t-stat of 2 or more, and the forecast-weighted gain before costs is positive.
- Reject: The mean next-bar return after active bars is at or above the baseline mean (difference ≥ 0), or the forecast-weighted gain is ≤ 0.
- Inconclusive: A difference below the baseline with a t-stat between 0 and 2 is inconclusive. So is any result from fewer than 60 active bars across all windows.
