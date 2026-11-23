---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.g2_weekend-rise-fades-early-week
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 6d77ef5ed57a
---
Fidelity:
- Situation: a coin rose from Saturday close to Sunday close, measured in its 20-day volatility of daily returns -> kept: the Sunday bar's one-bar return over the 20-bar std of daily returns, read only at the Sunday close (the coming bar is Monday).
- Comparison: the coin's normal drift -> kept: each case's 3-day return minus the coin's mean 3-day return over all windows.
- Outcome: falls behind its normal drift over the next 3 days, more so after a larger weekend rise -> kept: a short whose size grows with the scaled rise, held 3 bars.
- Verdict transfer: yes: the test measures the same scaled weekend rise and the same 3-day shortfall against drift, so a confirm or a reject carries over to the idea.
Forecast: A weekday rule sends the bar to the `mean_reversion` regime only at the Sunday close, when the coming bar is Monday. On every other bar the regime is `unknown`, which is null, so the forecast is 0. In the active regime the forecast is built in four steps: - The component is `VolatilityScaledReturnComponent` (period 1, vol_period 20): the Sunday bar's return divided by the std of the last 20 daily returns. - It is standardised over its past 60 values (min_periods 20), so a usual-sized move is about 10. - It is then negated and clipped at a maximum of 0. - The result is a short whose size grows linearly with the scaled weekend rise, capped at -20. It is 0 after a weekend fall or a flat weekend. The holding period keeps each Sunday bet for the 3-day horizon.
Config: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.g2_weekend-rise-fades-early-week_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: The cases are the Sunday-close bars with forecast < 0, one per week, so the cases do not overlap. For each case, take the coin's 3-day return from that close minus the coin's mean 3-day return over all its windows, with the sign flipped to the short's direction. The measure is the mean of this value weighted by |forecast|, with the t of the mean, before costs.
- Supporting check: Across the cases, the Pearson correlation between |forecast| and the shortfall (drift minus 3-day return) is above 0.
- Confirm: Both must hold: the weighted mean shortfall is above 0 with t >= 2, and the correlation is above 0.
- Reject: The weighted mean shortfall is below 0 with t <= -2, meaning weekend rises outrun their drift.
- Inconclusive: Anything else: |t| < 2, or t >= 2 with a correlation of 0 or below. At least 100 cases (Sunday rises) are required, otherwise the result is inconclusive.
