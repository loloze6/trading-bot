---
idea: 003-03_high-volume-up-move-continues
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a sharp up move on unusually high volume -> adapted: the volume condition becomes a regime that is on when volume is at or above its 20-bar mean, and the size of the current bar's rise sets the position.
- Comparison: volume judged against its usual level -> adapted: the only available test is "at or above its 20-bar mean", so "unusually high" becomes "above average".
- Outcome: price keeps rising afterwards -> adapted: the long is held only on the bar after the move, so the holding period is dropped.
- Verdict transfer: yes: the test is long in proportion to the size of the up move only on above-average-volume bars, so continuation confirms the idea and reversal rejects it.
Forecast: On any bar whose volume is at or above its 20-bar mean, the forecast is the bar's one-day percent rise divided by the average size of past one-day moves (60-bar window), times 10, and capped at 20. Down moves are clipped to 0, so the forecast is never short. It grows with how sharp the up move is. It is 0 on lower-volume bars, on down bars, and on the rare flat-volatility bar.
Config: 003-03_high-volume-up-move-continues_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Next-bar BTC return on bars with a non-zero forecast, weighted by the forecast, minus the mean next-bar return over all bars (the buy-and-hold drift), before costs. Each bar counts once across the 6 windows, so returns do not overlap.
- Supporting check: On active bars, take the top fifth by forecast. Their mean next-bar excess return should be positive and larger than that of the bottom fifth.
- Confirm: The forecast-weighted mean excess next-bar return is above 0 with a t-statistic of 2 or more.
- Reject: The forecast-weighted mean excess next-bar return is below 0 with a t-statistic of -2 or less (high-volume up moves give back).
- Inconclusive: A t-statistic between -2 and 2 is inconclusive. So is any result with fewer than 60 active bars across the 6 windows.
