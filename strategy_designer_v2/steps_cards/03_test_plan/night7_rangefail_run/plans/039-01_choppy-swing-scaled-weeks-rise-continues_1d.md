---
idea: 039-01_choppy-swing-scaled-weeks-rise-continues
brief: 039_choppy-market-swing-scaled-moves-continue
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: adf647c613f7
---
Fidelity:
- Situation: a coin in a choppy market, with its 20-day rise measured in its own 20-day daily swings -> kept (choppy is the brief's profile, built by code; the 20-day return is divided by the 20-day std of daily returns)
- Comparison: the rise against the coin's own daily swings -> kept
- Outcome: the larger the swing-scaled rise, the more it rises over the next 5 days -> kept (graded and signed, so a swing-scaled fall predicts a fall, as the brief states)
- Verdict transfer: yes: the forecast is the idea's own measure inside its own profile, held for its 5-day horizon.
Forecast: One component, `VolatilityScaledReturnComponent` with `period` 20, `vol_period` 20 and `lag` 0. It is the 20-day return divided by the std of the last 20 daily returns, times sqrt(20). The sqrt(20) is a constant and cancels under `standardise`. It is then standardised against its own last 60 values (min 20). The forecast is positive after a rise and negative after a fall, and its size grows with how many swings the move spans, up to the cap of 20. It is near 0 when the coin went nowhere. Step 3's code keeps it flat outside the choppy profile.
Config: 039-01_choppy-swing-scaled-weeks-rise-continues_1d_config.json
Profile: choppy (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The slope of the coin's 5-bar forward return, minus its normal drift over all windows, on the bar's forecast. Only bars with a nonzero forecast count, sampled on a non-overlapping 5-bar grid per window. Cases on the same day are pooled into one before the t is computed.
- Supporting check: The mean excess 5-bar return in the forecast's direction, over the same cases, is above 0.
- Confirm: The slope's t is 2 or more and the supporting check's mean is above 0.
- Reject: The slope's t is -2 or less: larger swing-scaled moves are followed by more reversal.
- Inconclusive: A slope t between -2 and 2, or a t of 2 or more with a mean in the forecast's direction at or below 0. Also inconclusive with fewer than 100 independent cases (grid days) in the choppy profile.
