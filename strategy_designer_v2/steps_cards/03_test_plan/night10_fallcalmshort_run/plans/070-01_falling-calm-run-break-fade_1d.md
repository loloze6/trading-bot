---
idea: 070-01_falling-calm-run-break-fade
brief: 070_falling-calm-run-break-fade
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: bd33e939b067
---
Fidelity:
- Situation: in a falling calm market, the first up day after a run of consecutive down days -> kept: a regime on the length of the down run broken by today's up close (2 or more down days), inside the falling calm profile added by code.
- Comparison: longer runs against shorter runs -> adapted: graded, so the short grows with the length of the run.
- Outcome: a fall over the next day, larger after longer runs -> kept: a short held for 1 daily bar.
- Verdict transfer: yes: the book is short only on those up days, sized by the run's length, and held for exactly the next day.
Forecast: `PriorDownRunOnUpCloseComponent` (`max_bars` 30, `side` "down", `form` "count") gives n, the length of the down run, on an up close that ends the run. It is 0 on every other bar. The regime detector selects `mean_reversion` when n is 2 or more (a run is at least two down days). Every other bar is `unknown`, which is flat. Inside the regime the same component is standardised (window 60, min_periods 20) and negated, so the forecast is always short. The component is 0 on about three bars in four, so its past mean size is about 0.5 while a case reads 2 or more. The standardise `target` is therefore set to 2, which keeps the forecast graded instead of pinned at the cap. A 2-day run gives about -8, 3 days about -12, 4 days about -16, and 5 or more days -20. The forecast is zero outside the situation and never positive. The code keeps the book flat outside the falling calm profile.
Config: 070-01_falling-calm-run-break-fade_1d_config.json
Side: short only (the brief): each component's forecast capped at 0 by step 3's code
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: Over the cases (bars with forecast below 0), the next-day return minus the coin's mean daily return over all windows, taken in the short direction. Its mean and its t, with the cases of one day summed together.
- Supporting check: Among the cases, the mean next-day excess return of runs of 3 days or more minus that of runs of exactly 2 days, using run length from `last_history_value`, is below 0.
- Confirm: The main measure's mean is above 0 with t ≥ 2, and the supporting difference is below 0.
- Reject: The main measure's t is ≤ -2 (up days after down runs are followed by rises beyond drift). Or the supporting difference's Welch t is ≥ +2 (longer runs are followed by weaker falls).
- Inconclusive: Anything else, including a main t between -2 and 2, or a main t ≥ 2 with a supporting difference at or above 0. At least 30 cases over at least 25 distinct days are needed, else inconclusive.
