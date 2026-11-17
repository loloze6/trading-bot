---
idea: 011-01_weekend-rise-reverses-monday
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the coin rose over the weekend, Saturday close to Sunday close -> adapted: the rise, read at the Sunday close, is made graded and the position is held only while the coming bar is Monday.
- Comparison: the larger the weekend rise, the larger the fall -> kept: the short grows with the size of the Sunday-bar return.
- Outcome: price falls over the next 2 days, Monday and Tuesday -> adapted: the Tuesday holding is dropped from the position, and the 2-bar fall is measured from the Sunday-close forecast.
- Verdict transfer: yes: the forecast at the Sunday close is exactly the graded weekend rise, and its 2-bar forward return is exactly the idea's Monday-Tuesday outcome.
Forecast: The regime detector reads the weekday of the coming bar. The forecast is active only at the close of the bar stamped Sunday, where the coming bar is Monday. On every other bar the forecast is 0. On that Sunday bar, the forecast is built from the Sunday bar's one-bar return (Saturday close to Sunday close, PriceEvolutionComponent with period 1). That return is standardised against the mean absolute size of the past 60 daily returns (min_periods 20), then negated, then clipped at a maximum of 0. The result: - After a weekend fall, the forecast is 0. - After a weekend rise, the forecast is a short that grows smoothly from 0 with the size of the rise, relative to the coin's usual daily move, capped at -20.
Config: 011-01_weekend-rise-reverses-monday_1d_config.json
Criterion:
- Horizon: 2 bars
- Main measure: - Cases: the bars stamped Sunday with forecast < 0. There is one case per week per coin, so the cases do not overlap. - Per case, the gain is (forecast / 10) x (close[t+2] / close[t] - 1 - m). Here m is the coin's mean 2-bar return over all windows, from the non-overlapping grid. - Measure: the mean of these gains, pooled over coins and windows, with the ordinary t of the mean.
- Supporting check: - Split the cases at the median of |forecast|. - Compute the excess 2-bar return (return minus m) of the large-forecast half minus the small-forecast half. - The check passes if this difference is below 0, meaning larger rises are followed by larger falls.
- Confirm: The idea is confirmed only if both hold: - the mean gain is above 0 with t >= 2; - the supporting check passes.
- Reject: The mean gain is below 0 with t <= -2. That means weekend rises continue into Monday-Tuesday, scaled by their size.
- Inconclusive: - Any t between -2 and 2 is inconclusive. - So is t >= 2 when the supporting check fails. - Fewer than 100 cases pooled is inconclusive whatever the result.
