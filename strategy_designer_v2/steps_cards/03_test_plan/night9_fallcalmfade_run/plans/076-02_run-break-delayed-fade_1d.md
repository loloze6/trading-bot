---
idea: 076-02_run-break-delayed-fade
brief: 076_run-break-fade-any-market
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 43e245a2b900
---
Fidelity:
- Situation: the first up day that ends a run of down days -> kept: the bar's own count of the down days it breaks, as a regime and as the graded size, zero on every other bar.
- Comparison: the fall is larger the more down days the run held -> kept: the short grows with the run's length.
- Outcome: the price falls on the second and third days after the up day -> kept: measured from the close one day after the up day to the close three days after it.
- Verdict transfer: yes: the measure reads exactly the day-2-to-3 move after each run break, and how it grows with the run's length.
Forecast: On every bar, `PriorDownRunOnUpCloseComponent` (count, `max_bars` 30) reads the number of down days that the day's up close breaks. It is 0 on down days, on flat days and on an up day that follows an up day. The regime detector selects the bars where it is 1 or more. Every other bar is flat. On those bars the count is standardised over the 60 bars before it (min 20). `target` is 2.5 because the count is zero on about three bars in four: with the default target every break would sit at the cap of 20. With 2.5 the size grows with the run: about 5 after one down day, 10 after two, and the cap of 20 is reached from about four down days. The result is negated, so the forecast is short only. It is 0 outside a run break and more negative the longer the broken run. Each bet is held for 3 bars, so the book covers days 1 to 3. The criterion reads days 2 and 3 only.
Config: 076-02_run-break-delayed-fade_1d_config.json
Side: short only (the brief): each component's forecast capped at 0 by step 3's code
Criterion:
- Horizon: 3 bars
- Main measure: The cases are bars with a negative forecast, read once per 3-bar grid cell. For each case, take the short-side excess return over days 2 and 3: minus (close[t+3]/close[t+1] - 1), less minus the coin's mean 2-day return over all windows. Average these returns weighted by abs(forecast). Compute t with the cases of one day taken together.
- Supporting check: The slope of that per-case excess short return on the run length (`last_history_value` of run_len), least squares, must be positive with t >= 2.
- Confirm: The weighted mean excess short return is above 0 with t >= 2, and the slope check passes (t >= 2).
- Reject: The weighted mean excess short return has t <= -2, or the slope has t <= -2.
- Inconclusive: Any other result. The test also counts as inconclusive with fewer than 300 cases or fewer than 200 distinct case days.
