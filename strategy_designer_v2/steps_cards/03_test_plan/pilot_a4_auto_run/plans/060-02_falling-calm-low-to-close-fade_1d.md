---
idea: 060-02_falling-calm-low-to-close-fade
brief: 060_falling-calm-wide-high-close-fade
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 7c1bf657fc4c
---
Fidelity:
- Situation: in a falling, calm market, a day whose close stands far above its low against the coin's 30-day daily swing -> kept: the profile comes from code, and "far above" is a regime at 2 usual moves or more (convention), measured as (close − low) / close / 30-day return std.
- Comparison: the distance measured against the coin's 30-day daily swing -> kept: the component divides by the std of the last 30 daily returns.
- Outcome: a fall over the next day, larger the further the close stands above the low -> adapted: a short position held 1 bar, graded by the distance inside the regime.
- Verdict transfer: yes: the config measures that distance on falling-calm days beyond the threshold and shorts more the further the close stands above the low, so a confirm or a reject of the next-day fall carries over to the idea.
Forecast: The forecast uses one indicator, VolatilityScaledDistanceFromHighComponent with period 1, vol_period 30, source "high", exclude_current 0, base "close" and extreme "low". It is the day's close above its low, as a share of the close, in usual 30-day daily moves. The regime detector selects mean_reversion only when this value is 2.0 or more. Every other bar is unknown (null), so the forecast is zero there. Inside the regime, the value is standardised against its own past 60 values and negated, so the forecast is always short or flat, never long. The short grows with the distance, up to the cap of 20. Code adds the falling-calm profile, which keeps the book flat outside that profile.
Config: 060-02_falling-calm-low-to-close-fade_1d_config.json
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: Take the bars with a short forecast (the cases). For each case, compute the coin's next-day return minus its mean daily return over all windows, signed for the short. Average this unusual move over the cases, with its t computed from the cases grouped by day, before costs.
- Supporting check: Split the cases at the median of the raw component (last_history_value). The upper half's mean unusual move minus the lower half's must be above 0.
- Confirm: The mean unusual move is positive (the coin falls more than usual), with a t of 2 or more, and the upper-half-minus-lower-half difference is above 0.
- Reject: The mean unusual move is negative (the coin rises more than usual), with a t of -2 or less.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t of 2 or more with the difference at or below 0 is also inconclusive. So is a sample with fewer than 30 distinct case days across all coins.
