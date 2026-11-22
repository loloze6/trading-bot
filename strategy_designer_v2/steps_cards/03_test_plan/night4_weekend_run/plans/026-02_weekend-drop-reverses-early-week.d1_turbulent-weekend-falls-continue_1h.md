---
idea: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 2a96c3272007
---
Fidelity:
- Situation: the coin fell over the weekend, Saturday 00:00 to Monday 00:00 UTC -> kept: the 48-bar return read once, at the close of the Sunday 23:00 bar, with only falls kept.
- Comparison: the weekend hours' volatility against the coin's previous week -> kept: the fall is scaled by the std of the 48 weekend hourly returns over the std of the 168 hourly returns before them.
- Outcome: the coin keeps falling over Monday and Tuesday, more so after a more volatile weekend -> kept: a short whose size grows with that product, held 48 bars.
- Verdict transfer: yes: the forecast is the idea's own weekend fall, its own volatility comparison and its own two-day horizon, so either verdict carries over.
Forecast: The forecast is computed once a week, at the close of the bar stamped Sunday 23:00 UTC. That bar is selected because the coming bar's weekday and hour are both 0. On that bar the component is `RecentToPriorVolatilityWeightedReturnComponent` (period 48, vol_period 48, base_period 168, base_lag 48). It gives the weekend's percent return, Saturday 00:00 to Monday 00:00, times the std of the weekend's 48 hourly returns over the std of the 168 hourly returns of the week before. It is standardised over its past 217 values (min_periods 54), then clipped at a maximum of 0. The forecast is negative (short) when the weekend fell and grows with both the size of the fall and how turbulent the weekend was against the prior week. It is 0 after a weekend rise. On all other bars the regime is null (forecast 0). The bet made on Monday 00:00 is held for the 48 bars of Monday and Tuesday.
Config: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: One case per coin per weekend where the Monday 00:00 forecast is at most -2. Per case, the value is |forecast|/10 × −(close[t+48]/close[t] − 1 − the coin's normal 48-bar drift). The drift is the mean 48-bar return over all windows, on non-overlapping stretches. The measure is the t of the mean of these values (cases do not overlap), judged before costs.
- Supporting check: Split the cases at the median |forecast|. The upper half's mean short-direction excess return, −(r − drift), must exceed the lower half's (difference upper minus lower > 0).
- Confirm: The main measure's t is 2 or more over at least 100 cases, and the supporting check passes.
- Reject: The main measure's t is -2 or less over at least 100 cases: weekend falls are followed by excess rises early in the week.
- Inconclusive: Any of the following is inconclusive: t between -2 and 2; fewer than 100 cases; or t of 2 or more while the supporting check fails.
