---
idea: 036-02_agitated-scaled-fall-delayed-rebound
brief: 036_agitated-fall-three-day-recovery
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: a coin's one-day fall, sized against its 30-day daily swing, in an agitated market -> kept: the fall day's return over the 30-day std of daily returns, only falls counted; the profile code adds the agitated condition.
- Comparison: the fall measured against the 30-day daily swing -> kept: `vol_period` 30 daily returns.
- Outcome: a larger rise over days 2 and 3 after the fall, leaving out day 1 -> kept: `lag` 1 reads the fall at the close of day 1, and the position is held from there for 2 bars.
- Verdict transfer: yes: the forecast is the idea's own graded fall size, held exactly over days 2 and 3, so a confirm or a reject carries over to the idea.
Forecast: `VolatilityScaledReturnComponent` with `period` 1, `vol_period` 30 and `lag` 1. At the close of bar t it reads the return of bar t-1, divided by the 30-day std of daily returns ending at t-1. The value is standardised (window 60, min_periods 20), then negated, then clipped at 0. The forecast is positive only when the day before was a fall, and it grows with that fall in usual daily moves; it is zero after an up or flat day and never goes negative. The bet is opened at the close of the day after the fall and held 2 bars, so it covers days 2 and 3. The profile code keeps the book flat outside agitated markets.
Config: 036-02_agitated-scaled-fall-delayed-rebound_1d_config.json
Profile: agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 2 bars
- Main measure: Use a non-overlapping 2-bar grid per window, taking only cells whose start bar has forecast > 0. Per cell, take the coin's 2-bar return close[t+2]/close[t]-1 minus the coin's mean 2-bar return over all windows. Regress that excess return on the forecast at t and read the slope's t-statistic.
- Supporting check: The forecast-weighted mean of those excess returns must be above 0, so the rise is credited beyond holding the coin.
- Confirm: The slope is positive with t ≥ 2 and the forecast-weighted mean excess return is above 0.
- Reject: The slope is negative with t ≤ -2.
- Inconclusive: A slope t between -2 and 2, or a confirming slope with a weighted mean excess of 0 or below. At least 100 grid cells with a positive forecast are needed; fewer is inconclusive.
