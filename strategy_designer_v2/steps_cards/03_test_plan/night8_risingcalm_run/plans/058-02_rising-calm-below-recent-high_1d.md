---
idea: 058-02_rising-calm-below-recent-high
brief: 058_rising-calm-pullbacks-recover
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 27e35f604dd2
---
Fidelity:
- Situation: in a rising, calm market, the close sits below its highest close of the past 5 days -> kept: the profile "rising calm" is added by code, and the distance below the 5-day closing high (bar t included) is measured as stated.
- Comparison: the distance measured against the usual daily swing, the 30-day std of daily returns -> kept: `VolatilityScaledDistanceFromHighComponent` divides by that std.
- Outcome: a larger rise over the next 5 days, growing with the scaled distance -> kept: long, graded by the distance, held 5 bars.
- Verdict transfer: yes: the forecast is the idea's own scaled dip inside its own profile, judged on its own 5-day horizon.
Forecast: The forecast uses one indicator. It takes (close − highest close of the last 5 daily closes, today included) / that high / std of the last 30 daily returns. That value is 0 at the high and negative below it. It is standardised over its past 60 values, then negated. The forecast is therefore 0 when the close is at its 5-day closing high and grows positive, long only, the deeper the close sits below that high in usual daily moves. It is capped at +20. It is never negative. Outside the rising calm profile, code keeps it flat.
Config: 058-02_rising-calm-below-recent-high_1d_config.json
Profile: rising calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The sample is in-profile bars (regime "unknown") on the non-overlapping 5-bar grid of each window. On those bars, regress the coin's 5-bar forward return minus its normal drift (its mean 5-bar return over all its windows) on the bar's forecast. The measure is the OLS slope's t, with cases of the same day taken together.
- Supporting check: On the same cases, the forecast-weighted mean excess 5-bar return is above 0.
- Confirm: The slope's t is 2 or more and the forecast-weighted mean excess return is above 0.
- Reject: The slope's t is -2 or less, meaning deeper scaled dips are followed by smaller or more negative excess returns.
- Inconclusive: A slope t between -2 and 2 is inconclusive. A slope t of 2 or more with a forecast-weighted mean excess return at or below 0 is also inconclusive. So is any result with fewer than 100 in-profile grid cases, or with fewer than 50 cases with forecast above 0.
