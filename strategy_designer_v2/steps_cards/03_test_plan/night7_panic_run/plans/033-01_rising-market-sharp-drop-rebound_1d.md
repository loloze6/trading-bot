---
idea: 033-01_rising-market-sharp-drop-rebound
brief: 033_dip-buying-in-rising-markets
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: a down day in a rising market, sized by its fall over the 30-day std of daily returns -> kept (the profile is added by code; zero on up days, graded by fall/std)
- Comparison: the fall against the coin's usual daily swing (30-day std) -> kept
- Outcome: the price rises over the next 3 days, more after a bigger scaled fall -> kept
- Verdict transfer: yes: the forecast is the idea's fall-in-usual-swings, held for 3 days, inside rising markets only.
Forecast: The forecast starts from the day's return divided by the standard deviation of the last 30 daily returns. It uses VolatilityScaledReturnComponent with period 1 and vol_period 30. That value is standardised against its own past 60 values, then negated and clipped at 0. So the forecast is 0 on up days and positive on down days, and it grows linearly with how many usual swings the day fell. It is long only. The code adds the rising profile, so the book is flat outside rising markets.
Config: 033-01_rising-market-sharp-drop-rebound_1d_config.json
Profile: rising (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: Use the in-profile bars, those with regime "unknown", on each window's non-overlapping 3-bar grid. Regress the coin's 3-day forward return, minus the coin's normal 3-day drift, on the forecast. Report the slope and its t.
- Supporting check: On the same grid, compute the mean 3-day forward return after bars with forecast > 0, minus the mean after in-profile bars with forecast = 0. This difference must be above 0.
- Confirm: Slope t ≥ 2, and the supporting difference is above 0.
- Reject: Slope t ≤ -2.
- Inconclusive: A slope t between -2 and 2, or t ≥ 2 with a difference at or below 0. At least 30 grid bars with forecast > 0 and at least 60 in-profile grid bars in total are needed. With fewer, the result is inconclusive.
