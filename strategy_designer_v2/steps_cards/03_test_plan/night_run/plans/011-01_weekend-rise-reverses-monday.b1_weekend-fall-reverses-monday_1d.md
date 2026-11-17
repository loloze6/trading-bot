---
idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the coin fell over the weekend, measured as its Saturday-to-Sunday close-to-close return -> kept: the Sunday bar's one-bar return, read only on that bar through a weekday regime.
- Comparison: the size of the fall relative to the coin's usual daily move -> kept: the return divided by the 20-bar standard deviation of daily returns.
- Outcome: price rises over the next 2 days (Monday and Tuesday), more after a deeper fall -> adapted: the 2-day hold is dropped, so the position covers Monday only; the 2-bar rise is still measured from prices.
- Verdict transfer: yes: the criterion measures the 2-bar forward return after each Sunday against the graded size of the fall, which is exactly what the idea claims.
Forecast: On the Sunday bar only, the regime detector selects mean_reversion. The coming bar is Monday, which `WeekdayComponent` reports as 0. On every other bar the forecast is 0. On the Sunday bar, the forecast is computed in four steps: - Start from that day's return over its 20-bar standard deviation of daily returns (`VolatilityScaledReturnComponent`, period 1, vol_period 20). - Standardise it against its own past 60 values. - Negate it, so a fall becomes positive. - Clip it at 0 from below, so the forecast is long only. The forecast is 0 after a weekend rise. It is positive after a weekend fall and grows linearly with the fall measured in usual moves, capped at 20. The position is held from Sunday's close to Monday's close.
Config: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday_1d_config.json
Criterion:
- Horizon: 2 bars
- Main measure: The sample is every Sunday bar (regime mean_reversion) with forecast > 0, pooled over coins and windows. Sundays are 7 bars apart, so the samples do not overlap. On these bars, regress the excess 2-bar return on the forecast: - The excess return is close[t+2]/close[t] − 1 minus the coin's mean 2-bar return over all its windows (non-overlapping grid). - The measure is the slope of that regression and its t-statistic.
- Supporting check: The forecast-weighted mean excess 2-bar return on those same bars is above 0.
- Confirm: The slope's t is 2 or more and the forecast-weighted mean excess 2-bar return is positive, with at least 200 cases.
- Reject: The slope's t is −2 or less, with at least 200 cases.
- Inconclusive: Any of these is inconclusive: - The slope's t is between −2 and 2. - The slope's t is 2 or more but the weighted mean excess return is 0 or below. - There are fewer than 200 Sunday-fall cases.
