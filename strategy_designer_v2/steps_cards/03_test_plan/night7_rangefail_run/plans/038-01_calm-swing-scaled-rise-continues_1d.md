---
idea: 038-01_calm-swing-scaled-rise-continues
brief: 038_calm-market-large-moves-continue
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: adf647c613f7
---
Fidelity:
- Situation: a coin's 5-day rise, counted in its 20-day daily swings -> kept: the 5-day return over the 20-day std of daily returns, rises only, graded by size.
- Comparison: the rise's size against the coin's own 20-day daily swings -> kept: dividing by that std is the comparison.
- Outcome: the coin rises more over the next 5 days, the larger the scaled rise -> kept: held 5 bars, judged by gains growing with position size.
- Verdict transfer: yes: the forecast is the idea's scaled rise held for its 5-day horizon inside the calm profile, so a graded continuation confirms it and a graded give-back rejects it.
Forecast: One component, VolatilityScaledReturnComponent (period 5, vol_period 20). It is the 5-day return divided by the 20-day standard deviation of daily returns times √5, which is the 5-day move counted in the coin's own daily swings. The component is standardised against its own past 60 values and then clipped at 0, so the forecast is long only. It is 0 when the last 5 days did not rise. It is positive after a rise and grows in proportion to how many daily swings the rise spans, capped at 20. The calm profile, added by code, keeps the book flat outside calm markets.
Config: 038-01_calm-swing-scaled-rise-continues_1d_config.json
Profile: calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The sample is the non-overlapping 5-bar grid of each window, using bars with forecast > 0. On it, regress the coin's 5-bar forward return minus its mean 5-bar return over all windows (the excess return) on the forecast. Report the slope's t, with cases on the same date pooled.
- Supporting check: On those grid bars, the mean 5-bar excess return is above 0.
- Confirm: The slope's t is 2 or more, and the supporting check's mean excess return is positive.
- Reject: The slope's t is -2 or less.
- Inconclusive: Any slope t between -2 and 2, or a confirming slope whose mean excess return is not positive, is inconclusive. Fewer than 100 grid cases with forecast > 0 is also inconclusive, whatever the t.
