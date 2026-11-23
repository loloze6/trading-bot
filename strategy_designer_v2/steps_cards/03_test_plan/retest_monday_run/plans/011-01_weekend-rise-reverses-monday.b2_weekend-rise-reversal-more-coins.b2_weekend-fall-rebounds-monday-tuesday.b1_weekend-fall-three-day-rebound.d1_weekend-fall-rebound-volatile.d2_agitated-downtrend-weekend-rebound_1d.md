---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile.d2_agitated-downtrend-weekend-rebound
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a weekend fall (Saturday-to-Sunday close-to-close return) while the 20-day return is negative, scaled by how far 20-day volatility sits above 60-day volatility -> kept
- Comparison: none -> kept
- Outcome: the coin rises over the next 3 days (Monday to Wednesday), more after larger falls and higher volatility ratios -> kept
- Verdict transfer: yes: the config bets only on Sunday closes of falling coins, sized by the weekend fall times the 20/60-day volatility ratio, and holds each bet for 3 days.
Forecast: The regime detector selects Sunday bars, meaning the coming bar is a Monday (WeekdayComponent = 0), on which the coin's 20-day return (PriceEvolutionComponent, period 20) is below 0. On every other bar the forecast is 0. On a selected bar the forecast is built in four steps: - It starts from RecentToPriorVolatilityWeightedReturnComponent with period 1, vol_period 20, base_period 60 and base_lag 0. This is Sunday's one-bar return in percent times (the standard deviation of the last 20 daily returns / the standard deviation of the last 60). - That value is standardised against its own past 60 daily values. - It is negated, so a fall reads positive. - It is clipped at 0, so the forecast is long only. The forecast is 0 on a Sunday that rose. It grows in proportion to the size of the weekend fall and to the 20/60-day volatility ratio, and it is capped at 20. Each Sunday bet is held for 3 bars (Monday to Wednesday closes).
Config: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile.d2_agitated-downtrend-weekend-rebound_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: A case is a Sunday bar with forecast of 2 or more. For each case, compute the coin's 3-day return from that close minus the coin's normal 3-day drift (its mean over non-overlapping 3-day stretches of all its windows). Take the forecast-weighted mean of these excess returns over all coins and windows, with its t-statistic. Cases are one week apart, so they do not overlap.
- Supporting check: The mean excess return of cases in the top half of forecast, minus that of cases in the bottom half, must be greater than 0.
- Confirm: The forecast-weighted mean excess 3-day return is positive with t ≥ 2, and the supporting check passes.
- Reject: The forecast-weighted mean excess 3-day return is negative with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t of 2 or more with the top-half minus bottom-half difference at 0 or below is also inconclusive. Fewer than 100 cases across all coins and windows makes the test inconclusive whatever the t.
