---
idea: 044-01_rising-market-wide-down-day-rebound
brief: 044_rising-market-wide-down-day-shakeout
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 18d3cc56dd45
---
Fidelity:
- Situation: a day that closes down, in a rising market -> adapted: "closes down" (close below the prior close) is a regime condition, graded inside it by the day's range; the rising profile is added by code.
- Comparison: the day's high-low range in units of the coin's 30-day standard deviation of daily returns -> kept: RangeInReturnStdComponent with vol_period 30.
- Outcome: price rises over the next 3 days, more the wider the range -> kept: long, held 3 bars, sized by the range.
- Verdict transfer: yes: the test bets long only on rising-market down days, sized by range per usual swing, for 3 days, which is exactly the idea's claim.
Forecast: The regime detector reads the day's 1-bar return (PriceEvolutionComponent, period 1, scaling_factor 1). When it is below 0 (a down close), the bar is `mean_reversion`; otherwise the bar is `unknown`, which is flat. On down-close bars the forecast is long. It equals the day's high-low range as a fraction of the close, divided by the 30-day standard deviation of daily returns (RangeInReturnStdComponent, vol_period 30). That value is standardised against its own last 60 values, so a typical day is about +10, a wide day is up to +20 and a narrow one is near 0. The range is never negative, so the forecast is never below zero. It is zero on up and flat days. The rising profile is added by code, which keeps the book flat outside rising markets.
Config: 044-01_rising-market-wide-down-day-rebound_1d_config.json
Profile: rising (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: The cases are bets (forecast rises of at least 2 points), one per 3-bar grid cell. For each case, the measure is the coin's 3-day return from the signal bar's close minus the coin's mean 3-day return over all windows. The measure is the mean of these excess returns, with its t computed with cases clustered by day.
- Supporting check: Least-squares slope of the case's excess 3-day return on its forecast (`post_pipeline_value` of range_std). The check passes when the slope is positive with t ≥ 1.
- Confirm: Mean excess 3-day return > 0 with t ≥ 2 over at least 100 cases, and the supporting check passes.
- Reject: Mean excess 3-day return < 0 with t ≤ -2 over at least 100 cases.
- Inconclusive: Any t between -2 and 2. Also inconclusive: a main t ≥ 2 while the slope check fails, or fewer than 100 cases.
