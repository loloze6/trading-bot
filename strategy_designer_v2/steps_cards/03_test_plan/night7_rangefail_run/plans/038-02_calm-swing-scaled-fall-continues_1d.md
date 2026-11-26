---
idea: 038-02_calm-swing-scaled-fall-continues
brief: 038_calm-market-large-moves-continue
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: adf647c613f7
---
Fidelity:
- Situation: a coin's 5-day fall, in a calm market -> kept: the 5-bar return, short side only (clip at 0); the calm profile is added by code.
- Comparison: the fall measured in the coin's 20-day daily swings -> kept: the return divided by the std of the last 20 daily returns (the constant √5 cancels under standardise).
- Outcome: the coin falls further over the next 5 days, more the larger the scaled fall -> kept: a graded short held for 5 bars.
- Verdict transfer: yes: the forecast is the scaled 5-day fall and grows with it, so a falling coin after large scaled falls confirms the idea, and a rise after them rejects it.
Forecast: The forecast is the 5-day return divided by the 20-day standard deviation of daily returns. It comes from VolatilityScaledReturnComponent with period 5 and vol_period 20. It is standardised against its own last 60 values, then clipped at a maximum of 0. It is negative (short) after a 5-day fall, and larger in size the more daily swings the fall spans, up to a cap of -20. It is zero after a 5-day rise or a flat stretch. It is never positive. The book is flat outside the calm profile (added by code).
Config: 038-02_calm-swing-scaled-fall-continues_1d_config.json
Profile: calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: Sample bars on a non-overlapping 5-bar grid per window, keeping bars with forecast < 0. Regress the coin's 5-bar forward return, minus its mean 5-bar return over all its windows, on the forecast. Report the slope's t, with same-day cases summed.
- Supporting check: On the grid bars with forecast ≤ -2, the mean short-side excess return (minus the excess return above) is above 0.
- Confirm: The slope is positive (deeper scaled falls are followed by lower excess returns) with t ≥ 2, and the supporting check is positive.
- Reject: The slope is negative with t ≤ -2 (deeper scaled falls are followed by higher excess returns).
- Inconclusive: A slope t between -2 and 2, or a confirming slope with a non-positive supporting check. Also inconclusive with fewer than 100 grid cases with forecast < 0, or fewer than 30 with forecast ≤ -2.
