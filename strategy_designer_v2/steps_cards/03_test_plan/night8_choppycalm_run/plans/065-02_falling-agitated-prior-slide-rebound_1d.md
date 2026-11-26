---
idea: 065-02_falling-agitated-prior-slide-rebound
brief: 065_agitated-downtrend-slide-depth-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 4510fe2da56d
---
Fidelity:
- Situation: a falling, agitated market with a fall over the four days before the latest day -> kept: the profile is added by code, and the depth is the negated 4-day return ending at the prior close (lag 1), clipped at 0
- Comparison: the slide's depth against the latest day's own fall -> kept: the latest day's return is rebuilt from closes and set beside the depth in the check
- Outcome: a larger rise over the next day for a deeper slide -> kept: the next 1-day return, long, graded by depth
- Verdict transfer: yes: the forecast is the idea's slide depth and nothing else, held for one day inside the profile, so a confirm or a reject is about the idea.
Forecast: The forecast uses one indicator, VolatilityScaledReturnComponent with period 4, lag 1, vol_period 20 and vol_lookback 365. Its value is the return from close[t-5] to close[t-1], the four days before the latest day. It is divided by the coin's past-year average 20-day swing, which changes slowly, so the reading stays close to a percent depth. The value is standardised against its own past 386 values, then negated and clipped at 0. The forecast is therefore zero when those four days did not fall. It is positive after a fall, and it grows in proportion to the depth of the fall, up to the cap of 20. The latest day's own move does not enter the forecast. The forecast is long only. Code keeps the book flat outside the falling agitated profile.
Config: 065-02_falling-agitated-prior-slide-rebound_1d_config.json
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: The slope of the next-day excess return on the forecast, pooled over all coins and over bars with forecast > 0. The excess return is close[t+1]/close[t]-1 minus the coin's mean daily return over all windows. The t uses standard errors clustered by day.
- Supporting check: The same regression with the latest day's return (close[t]/close[t-1]-1) added as a second regressor. The forecast's slope must stay positive with t ≥ 2.
- Confirm: The main slope is positive with t ≥ 2, and the supporting check passes.
- Reject: The main slope is negative with t ≤ -2.
- Inconclusive: These results neither confirm nor reject: - a main t between -2 and 2; - a main t ≥ 2 with a failed check; - fewer than 100 bars with forecast > 0, or those bars falling on fewer than 50 distinct days.
