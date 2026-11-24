---
idea: 031-01_up-streak-length-reversal
brief: 031_daily-close-streak-reversal-or-continuation
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 8342b7be17d6
---
Fidelity:
- Situation: days in a row a coin has closed higher -> kept
- Comparison: against its own up-close streak lengths over the past 365 days -> kept
- Outcome: the longer the streak, the more it falls over the next 5 days -> adapted: graded short position, sized by the streak's rank, held 5 days
- Verdict transfer: yes: the forecast is a short sized by the current up-streak's rank among the coin's completed up-streaks of the past 365 days, held 5 days, so both its confirm and its reject speak to the idea.
Forecast: One component, UpCloseStreakLengthComponent (side "up", base "rank", base_window 365, max_bars 30). Its value is the share of the coin's completed up-close streaks in the past 365 days that are no longer than the current streak. It is standardised over its past 366 values (min_periods 91), then negated. The forecast is 0 on any day that did not close higher. On an up-close day it is negative (short), and it grows in size as the current streak ranks longer against the coin's own streaks. It is never positive.
Config: 031-01_up-streak-length-reversal_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The mean unusual move per case, in the short direction. A case is a short bet (a fall of the forecast of at least 2 points), read once per 5-bar grid cell. The unusual move is the coin's 5-bar return from the signal bar minus its normal 5-bar drift, so holding the coin is the benchmark. Its t is computed with cases clustered by day, before costs.
- Supporting check: The mean unusual move in the short direction of cases in the top third of |forecast| must exceed that of the bottom third.
- Confirm: The main measure's t is 2 or more, on at least 100 cases over at least 30 days, and the supporting check passes.
- Reject: The main measure's t is -2 or less, meaning up streaks are followed by rises beyond the drift, on at least 100 cases over at least 30 days.
- Inconclusive: A t strictly between -2 and 2, a confirm-level t whose supporting check fails, or fewer than 100 cases or 30 days.
