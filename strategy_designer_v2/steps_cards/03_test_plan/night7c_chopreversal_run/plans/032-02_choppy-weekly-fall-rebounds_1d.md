---
idea: 032-02_choppy-weekly-fall-rebounds
brief: 032_agitated-chop-weekly-reversal
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 051b3422f169
---
Fidelity:
- Situation: the coin has been choppy over the past 30 days, with large daily swings both ways and little net progress -> adapted: a regime condition. The 30-day efficiency ratio must be 0.3 or less (the Kaufman chop convention). The 30-day volatility must be at or above its one-year median (the "large swings" part).
- Comparison: the 7-day fall measured against the coin's typical daily swing over the past 30 days -> kept: the 7-day return divided by the 30-day standard deviation of daily returns.
- Outcome: the 7-day fall is partly recovered by a rise over the next 7 days, larger after larger falls -> kept: a long position graded by fall size, held 7 bars.
- Verdict transfer: yes: the test bets on exactly the stated rebound, only in the stated chop, sized by the stated scaled fall, over the stated horizon.
Forecast: The forecast is computed only on bars where both conditions hold: - the 30-day efficiency ratio (raw, unsmoothed) is 0.3 or less; - the 30-day volatility ranks at or above 0.5 among the last 365 days. On every other bar the forecast is 0, so the book is flat. Inside the regime, the forecast comes from the 7-day return divided by the 30-day daily-return standard deviation times √7. It is standardised over its past 60 values (target 10), negated, and clipped at 0. It is therefore positive only after a 7-day fall, grows with the depth of that fall in typical daily swings, is 0 after a rise, and never goes short.
Config: 032-02_choppy-weekly-fall-rebounds_1d_config.json
Criterion:
- Horizon: 7 bars
- Main measure: Use non-overlapping 7-bar grid cells (one grid per window). The cases are cells where the regime is mean_reversion and the forecast is above 0. For each case, take the coin's 7-bar forward return minus the coin's mean 7-bar return over all windows, and regress it on the forecast. The measure is the slope's t, with cases on the same day taken together.
- Supporting check: The mean excess 7-bar return over those cases (the rebound minus holding the coin) is above 0.
- Confirm: Both of these hold: - the slope's t is 2 or more; - the mean excess return of the cases is positive.
- Reject: Either of these: - the slope's t is -2 or less; - the mean excess return has t of -2 or less (the falls continue).
- Inconclusive: The results in between, i.e. a slope t between -2 and 2, or a positive slope with a mean excess return of 0 or below. A test with fewer than 40 cases on distinct days is also inconclusive.
