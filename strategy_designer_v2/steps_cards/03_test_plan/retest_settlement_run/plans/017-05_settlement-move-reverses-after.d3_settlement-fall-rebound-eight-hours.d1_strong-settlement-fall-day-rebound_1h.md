---
idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a fall over the 2 hours before the 00:00 or 16:00 UTC settlement -> kept: a clock regime selects the bars closing at 00:00 and 16:00, and the forecast reads the 2-bar return ending there.
- Comparison: the fall against the coin's usual 2-hour move -> kept: the 2-hour return is divided by the mean absolute 2-hour return of the last 720 bars.
- Outcome: a rise over the 24 hours after, larger for larger falls, carried by the largest falls -> kept: long bets held 24 bars, graded with a cubic dead zone.
- Verdict transfer: yes: the test buys exactly the settlement falls, sized by their scaled depth, and holds each for the idea's day.
Forecast: The forecast is non-zero only on the bars whose close is a 00:00 or 16:00 UTC settlement. On those bars the coming bar starts at hour 0 or 16, and a threshold-rules regime on HourOfDayComponent selects them. Every other bar is flat. On a settlement bar it starts from MeanAbsScaledReturnComponent (period 2, window 720): the 2-hour return in usual 2-hour moves. This value is standardised (window 500, min_periods 120), then negated, so that a fall reads positive. It is then clipped at 0, so the test is long only and buys falls only. Finally signed_power with exponent 3 (pivot 10) is applied. A fall of about one usual size gives a small position. A fall of twice the usual size or more reaches the +20 cap. A rise or no fall gives 0. Each bet is held 24 bars.
Config: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: A case is a settlement bar where the forecast reaches 2 or more. Take at most one case per 24-bar grid cell of each window, choosing the largest forecast in the cell. For each case, measure the coin's 24-bar return from that bar's close minus the coin's mean 24-bar return over all windows. Report the forecast-weighted mean of these excess returns, and the ordinary t of the case excess returns, before costs.
- Supporting check: The mean excess 24-bar return of cases with forecast at or above 10 exceeds that of cases with forecast from 2 to below 10. This shows that the largest falls carry the rebound.
- Confirm: The weighted mean excess return is above 0 with t ≥ 2. The supporting check must also pass.
- Reject: The weighted mean excess return is below 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A confirming t with a failed supporting check is also inconclusive. Fewer than 30 cases across all coins and windows is inconclusive, whatever the t.
