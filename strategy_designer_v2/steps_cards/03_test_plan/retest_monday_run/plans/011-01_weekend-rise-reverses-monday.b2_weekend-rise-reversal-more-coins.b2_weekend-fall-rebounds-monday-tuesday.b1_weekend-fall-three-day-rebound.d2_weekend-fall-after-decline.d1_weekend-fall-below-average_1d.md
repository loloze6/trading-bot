---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d1_weekend-fall-below-average
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: the coin's Saturday-to-Sunday close-to-close fall, larger the fall, with its Sunday close below its 50-day average, more the further below -> adapted: the weekend fall and the close below the 50-day SMA are regime conditions; the forecast grows with the fall's size plus the depth below the SMA.
- Comparison: coins above their 50-day average are refused -> kept: the regime is flat when the Sunday close is at or above the 50-day SMA.
- Outcome: the price rises over the next 3 days (Monday to Wednesday) -> kept: the bet is set at Sunday's close and held 3 daily bars.
- Verdict transfer: yes: the test measures the idea's own weekend fall, its own 50-day gate and depth, and its own 3-day rise.
Forecast: The forecast is set only on the Sunday bar, when the coming bar is a Monday. On that bar the Sunday one-bar return must be negative and the close must be below its 50-day SMA. On all other bars the forecast is 0. When the regime is active, the forecast is the equal-weight mean of two parts. The first is the Sunday fall: the 1-bar percent return, standardised over 60 bars and negated. The second is the depth below the 50-day SMA: the percent distance, standardised over 60 bars and negated. Both parts are clipped at 0, so the forecast is never short. It is positive and grows with the size of the weekend fall and with how far the close sits below the average. The holding period keeps the bet over Monday to Wednesday.
Config: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.d1_weekend-fall-below-average_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: A case is a Sunday bar with forecast > 0. For each case, take the coin's 3-bar return from that close (close[t+3]/close[t]-1) minus the coin's mean 3-bar return over all its windows. Multiply it by forecast/10. The measure is the t of the mean of this product over all cases. Cases are one per week, so they do not overlap.
- Supporting check: The least-squares slope of the cases' excess 3-bar return on their forecast must be above 0.
- Confirm: The mean forecast-weighted excess return has t ≥ 2 over at least 100 cases, and the slope check is above 0.
- Reject: The mean forecast-weighted excess return has t ≤ -2 over at least 100 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t ≥ 2 with a slope ≤ 0 is also inconclusive. Any result from fewer than 100 cases is inconclusive.
