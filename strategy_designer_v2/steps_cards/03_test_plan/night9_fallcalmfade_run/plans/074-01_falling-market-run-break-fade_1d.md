---
idea: 074-01_falling-market-run-break-fade
brief: 074_falling-market-run-break-fade
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 607e0219f5c3
---
Fidelity:
- Situation: in a falling market, the first up day after a run of consecutive down days -> kept: the falling profile is added by code, and a regime rule fires on an up close that ends a run of 2 or more down closes.
- Comparison: the next day against other days, and stronger after longer runs -> kept: the next-day return is judged against the coin's normal drift, and graded by run length.
- Outcome: the close falls over the next day, more after longer runs -> kept: a short position held 1 bar, sized by the run length.
- Verdict transfer: yes: the book is short exactly on run-ending up days in falling markets, sized by run length, and held for the stated next day.
Forecast: The forecast uses PriorDownRunOnUpCloseComponent (max_bars 30). It reads n, the number of down closes that today's up close breaks, and is 0 on every other bar. The regime detector selects mean_reversion only when n is 2 or more. On every other bar the regime is unknown, which is set to null, so the book is flat. Inside the regime the forecast is -n standardised against the mean absolute value of the last 60 stored values. Those stored values are mostly zeros, and run-ending days are about 1 bar in 4. The target is therefore 2, which puts a typical event on the forecast scale. A run of 2 gives about -8, 3 about -12, 4 about -16, and 5 or more reaches the -20 cap. The forecast is never positive (short only), and it is 0 outside the event and outside the falling profile.
Config: 074-01_falling-market-run-break-fade_1d_config.json
Side: short only (the brief): each component's forecast capped at 0 by step 3's code
Profile: falling (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: On bars where the forecast is below 0, take minus the next-day return (close[t+1]/close[t]-1) minus the coin's mean daily return over all windows, so the mean is the short-side unusual move. Its t clusters same-day cases across coins.
- Supporting check: Among those cases, the mean short-side unusual move after runs of 3 or more must exceed the mean after runs of exactly 2 (run length read from the forecast size or recomputed from closes).
- Confirm: The main measure is positive with t of 2 or more, and the supporting check passes (difference above 0).
- Reject: The main measure has t of -2 or less: next days are stronger than the coin's drift.
- Inconclusive: Any t between -2 and 2, or a confirming t with a failed supporting check, is neither a confirm nor a reject. At least 30 cases on distinct days are needed, else inconclusive.
