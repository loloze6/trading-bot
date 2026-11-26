---
idea: 074-01_rising-calm-wide-low-close-rebound
brief: 074_rising-calm-wide-low-close-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 607e0219f5c3
---
Fidelity:
- Situation: in a rising calm market, a day with a wide range against its 30-day return swing that closes near its low -> adapted: the profile is added by code; "wide" (range at least 2 swings) and "near its low" (close in the lower third of the range) are a regime, graded inside it by range in swings times nearness to the low.
- Comparison: the day's high-to-low range against the coin's 30-day standard deviation of daily returns -> kept.
- Outcome: the price rises over the next day, more so for a wider day closer to its low -> kept.
- Verdict transfer: yes: the test measures the stated situation, comparison and next-day rise, and grades the position by the idea's own strength.
Forecast: The forecast is zero on every bar unless two conditions hold. First, the day's range as a share of the close, divided by the 30-day standard deviation of daily returns, is at least 2. Second, the close sits in the lower third of the day's range, measured from the high. On those days the forecast is long and graded. It uses VolatilityScaledDistanceFromHigh (period 1, source high, base close, vol_period 30), negated. That value is (high − close)/close/s, which equals the range in swings times the nearness to the low. It is standardised against its past 60 values. The standardise target is 5 instead of 10, so qualifying days are not pinned at the +20 cap. The forecast grows as the day gets wider and closes closer to its low, and it is never short. Code adds the rising-calm profile, so the book is flat outside it.
Config: 074-01_rising-calm-wide-low-close-rebound_1d_config.json
Profile: rising calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: The case is a bar with a forecast above 0, and the result is its next-day return minus the coin's mean daily return over all windows. The cases of one day are pooled into one piece of evidence, and the measure is the t of the mean, before costs.
- Supporting check: Across the cases, the correlation between the forecast and that next-day excess return is above 0.
- Confirm: The mean excess next-day return is above 0 with t ≥ 2, and the correlation with the forecast is above 0.
- Reject: The mean excess next-day return has t ≤ -2, or the correlation is below 0 with t ≤ -2.
- Inconclusive: Any result with |t| < 2 is inconclusive, as is a positive mean whose correlation is not above 0. So is any test with fewer than 30 distinct case days.
