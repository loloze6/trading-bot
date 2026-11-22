---
idea: 025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins
brief: 025_bounces-fade-in-falling-markets
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: the 90-day return is negative and there was just a one-day rise of several usual daily moves -> kept: a regime rule fires on the bounce bar when the 90-day return is below 0 and the vol-scaled 1-day return is at least 2.
- Comparison: the deeper its 90-day fall, the larger the fall that follows -> kept: inside the regime, the short is sized by the depth of the 90-day fall.
- Outcome: the coin falls over the next 5 days -> kept: a short held for 5 daily bars.
- Verdict transfer: yes: the test measures the stated bounce condition, sizes the bet by the stated depth and judges the stated 5-day fall.
Forecast: The regime detector selects `mean_reversion` only on a bar where both conditions hold. The 90-day price change (PriceEvolutionComponent, period 90) must be below 0. The day's return divided by the 20-day standard deviation of daily returns (VolatilityScaledReturnComponent, period 1, vol_period 20) must be at least 2. On every other bar the forecast is 0. On a selected bar the forecast is the 90-day return standardised against its own past 90 values, which is always negative there. It is clipped at 0 from above, so the forecast is short only. Its size grows with the depth of the 90-day fall: near 0 for a shallow fall, about -10 for a fall of usual size, and down to -20 for a deep one. Each bet is held for 5 bars.
Config: 025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Use the cases: bars in regime `mean_reversion` with a short bet, one per 5-bar grid cell of each window. Across these cases, regress the coin's 5-day return minus the coin's mean 5-day return over all windows on the 90-day return (`fall_depth` last_history_value). The measure is the slope's t.
- Supporting check: Take the cases' 5-day return minus the coin's mean 5-day return, in the short direction. Its mean must be above 0.
- Confirm: The slope is positive (a deeper 90-day fall is followed by a more negative excess 5-day return) with t ≥ 2. The supporting check must also pass, over at least 50 cases.
- Reject: The slope is negative (a deeper fall is followed by a smaller fall or a rise) with t ≤ -2, over at least 50 cases.
- Inconclusive: A slope t between -2 and 2 is inconclusive. So is a slope t ≥ 2 when the case mean in the short direction is not above 0. Fewer than 50 non-overlapping cases is also inconclusive.
