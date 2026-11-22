---
idea: 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends.b1_panic-rebound-more-coins
brief: 027_panic-days-are-followed-by-a-premium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: a 24-hour stretch (6 bars) whose range is several times its 30-day average, with a coin falling over it -> kept: a regime rule fires when the 6-bar range is at least 7.5 mean 4h bar ranges over 180 bars, which is 3 times a usual 24h range of about 2.5 bar ranges; the fall depth is the 6-bar fall in usual 6-bar moves.
- Comparison: the deeper the fall, the higher the return, only while the 90-day (540-bar) return is positive, more so the larger the rise -> kept: the forecast is the fall depth times the positive 540-bar return, and it is 0 when that return is not positive.
- Outcome: a higher return over the next 14 days (84 bars), up -> kept: long, held 84 bars, judged against the coin's normal 84-bar drift.
- Verdict transfer: yes: the test is long only in panic stretches of rising coins, sized by fall depth times the 90-day rise, and it measures the following 14-day excess return.
Forecast: Every bar is classified by the 6-bar high-low range measured in mean 4h bar ranges over the last 180 bars. When that ratio is 7.5 or more (a panic stretch), the forecast is MeanAbsScaledFallTimesRiseComponent with fall_period 6, window 180 and rise_period 540. Its raw value is the 24h fall in usual 24h moves times the positive 90-day percent return. That value is standardised over its last 500 values, then passed through signed_power with exponent 3 so that small readings are damped toward 0. The forecast is long only and grows with the fall's depth and the 90-day rise. It is 0 when the coin did not fall, when its 90-day return is not positive, or outside panic stretches.
Config: 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends.b1_panic-rebound-more-coins_4h_config.json
Criterion:
- Horizon: 84 bars
- Main measure: The mean unusual move per case. A case is a long bet of at least 2 forecast points, read once per 84-bar grid cell. Its unusual move is the coin's 84-bar return from the signal bar's close minus the coin's normal 84-bar drift over all windows. Its t is the ordinary t of the mean over the cases.
- Supporting check: Split the cases at the median forecast at the signal. The mean unusual move of the upper half minus that of the lower half must be above 0.
- Confirm: The mean unusual move is positive with t >= 2, and the upper-half-minus-lower-half difference is above 0.
- Reject: The mean unusual move is negative with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive, and so is t >= 2 when the supporting check fails. Fewer than 30 cases over all coins and windows is inconclusive whatever the t.
