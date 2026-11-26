---
idea: 058-02_calm-range-bottom-drifts-up
brief: 058_choppy-calm-range-edge-reversion
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 4510fe2da56d
---
Fidelity:
- Situation: the close's nearness to the bottom of its 20-day high-low range, in a choppy calm market -> kept. The range position is graded, and the profile is added by code.
- Comparison: nearer the bottom against farther from it -> kept. The position grows as the close nears the range's low.
- Outcome: a larger rise over the next 5 days -> kept. The book holds for 5 bars, judged against the coin's normal drift.
- Verdict transfer: yes: a forecast growing with nearness to the bottom tests exactly whether nearer-bottom closes rise more over 5 days.
Forecast: The forecast is built from one component, the position of the close inside its 20-day high-low range (`DonchianBreakoutComponent`, period 20, source "high_low", current bar included). This value is -sf at the range's low, 0 at the middle and +sf at the high. - It is standardised over its past 60 values (min_periods 20), then negated, so it is positive below the middle of the range. - It is then clipped at 0, so the forecast is long-only. - The forecast is 0 at or above the middle of the range. Below the middle it is positive and grows linearly as the close nears the range's low, up to the cap of 20. - Code adds the choppy calm profile. Outside that profile the book is flat.
Config: 058-02_calm-range-bottom-drifts-up_1d_config.json
Profile: choppy calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: The slope of the coin's 5-bar forward return on the forecast. The return is taken minus the coin's mean 5-bar return over all windows. The bars used are the profile's bars on a non-overlapping 5-bar grid in each window, pooled over the coins, with the t-statistic of the slope.
- Supporting check: The mean excess 5-bar return of the grid cases with forecast above 0 is positive.
- Confirm: The slope is positive with t ≥ 2, and the supporting check passes.
- Reject: The slope is negative with t ≤ -2.
- Inconclusive: Any slope with t between -2 and 2, or a positive slope with a failed check, is inconclusive. Fewer than 50 grid cases with forecast above 0 is also inconclusive.
