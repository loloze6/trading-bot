---
idea: 066-02_falling-agitated-year-scaled-fall-rebound
brief: 066_longer-swing-yardstick-agitated-fall-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 4510fe2da56d
---
Fidelity:
- Situation: a one-day fall, large against the std of daily returns over the last 365 days, in a falling agitated market -> adapted: "large" made graded (the larger the fall in yearly swings, the larger the long), with the profile added by code.
- Comparison: the fall judged against the past year's daily swing -> kept: the day's return is divided by the 365-day std of daily returns.
- Outcome: a rise the next day, larger after larger falls -> kept: a long held 1 bar, sized by the fall.
- Verdict transfer: yes: the forecast is the idea's scaled fall inside its profile, held for its one-day horizon.
Forecast: The forecast uses VolatilityScaledReturnComponent with period 1 and vol_period 365. This is the day's return divided by the std of the last 365 daily returns. The forecast has four steps: - It is standardised against its own past 365 values. - It is negated, so a fall reads positive. - It is clipped at 0, so the forecast is 0 on up days and long only. - signed_power with exponent 2 is applied, a graded dead zone: small falls give almost nothing, and the long grows with the square of the fall's size in yearly swings. The book is flat outside the falling agitated profile, which code adds.
Config: 066-02_falling-agitated-year-scaled-fall-rebound_1d_config.json
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bars
- Main measure: The sample is the bars with forecast > 0. On each, the next-day return close[t+1]/close[t]-1 minus the coin's mean daily return over all windows is regressed on the forecast. The slope's t is computed with the cases of one day pooled.
- Supporting check: The mean next-day excess return over the same bars is above 0.
- Confirm: The slope's t is 2 or more and the mean excess return is above 0.
- Reject: The slope's t is -2 or less.
- Inconclusive: A slope t between -2 and 2 is inconclusive. A positive slope with a mean excess return at or below 0 is also inconclusive. So is any result from fewer than 100 bars with forecast > 0, or from fewer than 60 distinct days.
