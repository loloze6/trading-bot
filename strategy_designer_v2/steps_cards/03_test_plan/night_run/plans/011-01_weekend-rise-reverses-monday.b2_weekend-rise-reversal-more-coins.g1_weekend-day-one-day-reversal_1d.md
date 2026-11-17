---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g1_weekend-day-one-day-reversal
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: a coin's one-day return on a Saturday or Sunday, against its own recent daily volatility -> kept
- Comparison: weekday moves of similar size are not reversed the same way -> kept
- Outcome: the weekend day's move is reversed over the next day, in proportion to its size -> kept
- Verdict transfer: yes: a weekend-only, size-graded one-day fade, checked against the same fade on weekdays, is exactly the idea.
Forecast: The forecast is active only when the bar just closed is a Saturday or a Sunday. `WeekdayComponent` reads the coming bar, so the regime fires when the coming bar is Sunday (6) or Monday (0). On those bars the forecast is minus the bar's one-day return divided by the standard deviation of the last 20 daily returns (`VolatilityScaledReturnComponent`, period 1, vol_period 20). It is standardised against its own past 60 values, then negated. It is positive after a weekend fall and negative after a weekend rise, and its size grows with how unusual the move was. On every weekday bar the forecast is 0.
Config: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g1_weekend-day-one-day-reversal_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On weekend bars (regime mean_reversion), pool all coins and windows and take the position's gain over holding the coin. For each bar this is postRebalance_current_allocation x (close[t+1]/close[t] - 1 - the coin's mean daily return over all windows). Measure its mean and t, one independent case per bar.
- Supporting check: Compute the per-unit fade -z_t x (r_{t+1} - the coin's mean daily return). Here z_t is the vol-scaled one-day return recomputed from closes with a 20-day volatility. Compare it on weekend bars against weekday bars using Welch's t, weekend minus weekday.
- Confirm: The main measure's t is ≥ 2 and the supporting check's t is ≥ 2.
- Reject: The main measure's t is ≤ -2, or the supporting check's t is ≤ -2.
- Inconclusive: Every other result is inconclusive, including any t between -2 and 2. Either test needs at least 300 weekend bars and 300 weekday bars; with fewer, the result is inconclusive.
