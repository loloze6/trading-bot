---
idea: 060-02_falling-agitated-rally-fades-next-day
brief: 060_falling-agitated-scaled-rise-giveback
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 4510fe2da56d
---
Fidelity:
- Situation: a one-day rise, in a falling agitated market -> kept: the profile comes from the header, and inside it a short is graded by the size of the rise on up days only.
- Comparison: the rise against the std of daily returns over the past 30 days -> kept: the 1-day return over the 30-day return std, today's return included.
- Outcome: a larger fall over the next day -> kept: short for one bar, larger after a larger scaled rise.
- Verdict transfer: yes: the test measures whether larger scaled up days are followed by larger next-day falls inside the profile, which is the idea as stated.
Forecast: The indicator is the day's return divided by the standard deviation of the last 30 daily returns (VolatilityScaledReturnComponent, period 1, vol_period 30). It is standardised over its past 60 values, so a typical move reads about 10 and the value is capped at 20. It is then clipped at 0, so down days and flat days give 0, and negated. The forecast is therefore 0 after a down or flat day and negative after an up day, growing in size with the rise measured in 30-day swings. It is never positive. Outside the falling agitated profile, code keeps the book flat.
Config: 060-02_falling-agitated-rally-fades-next-day_1d_config.json
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bars
- Main measure: Use the bars with a negative forecast (the cases). For each case, take the coin's next-day return minus its mean daily return over all windows, and flip its sign so that a fall counts as a gain for the short. Regress this signal-direction excess return on |forecast|. Report the slope's t, clustering the cases of the same day together.
- Supporting check: The mean signal-direction excess return over the same cases, with its t, cases of one day taken together.
- Confirm: The slope's t is 2 or more, and the mean signal-direction excess return is above 0 with a t of 2 or more.
- Reject: The slope's t is -2 or less, or the mean signal-direction excess return has a t of -2 or less (up days followed by returns above usual).
- Inconclusive: Any result in between, including slopes or means near zero. Fewer than 100 cases, or cases on fewer than 50 distinct days, is also inconclusive whatever the t.
