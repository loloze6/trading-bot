---
idea: 077-03_choppy-agitated-close-position-reversal
brief: 077_choppy-agitated-wide-close-fade
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: eeccfd98cf40
---
Fidelity:
- Situation: a day in a choppy, agitated market, closing away from its range's middle -> kept: the profile is added by code, and the close's signed distance from mid-range is measured on each day.
- Comparison: the distance from the middle times the day's range against its 30-day swing -> kept: CloseOffMidRangeInUsualMovesComponent (vol_period 30) computes exactly this product.
- Outcome: the next day moves against the close's side, larger with that product -> kept: negated forecast, horizon 1 bar.
- Verdict transfer: yes: the forecast is the idea's own product with the idea's sign, inside the idea's profile, held for its one-day horizon.
Forecast: One component, CloseOffMidRangeInUsualMovesComponent with vol_period 30. It computes 2 x (close − mid-range) / close / s, where s is the 30-day standard deviation of daily returns. This is the close's distance from the day's middle times the day's range in usual daily moves. The value is standardised over its past 60 values (min_periods 20), then negated. The forecast is long after a day closing below its middle and short after one closing above it. It is 0 at mid-range, and its size grows with both the distance from the middle and the day's width. No regime of its own: step 3's code adds the choppy agitated profile and keeps the book flat outside it.
Config: 077-03_choppy-agitated-close-position-reversal_1d_config.json
Profile: choppy agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: The least-squares slope of the next-day excess return on the forecast, over bars with a non-zero forecast. The excess return is close[t+1]/close[t] − 1 minus the coin's mean daily return over all windows. The slope's t is computed with the cases of one day taken together.
- Supporting check: On the third of in-position bars with the largest |forecast|, the mean next-day excess return in the forecast's direction is above 0.
- Confirm: The slope's t is 2 or more, and the supporting check passes.
- Reject: The slope's t is −2 or less.
- Inconclusive: A slope t between −2 and 2, or a t of 2 or more with a failed check, is inconclusive. Fewer than 300 in-position bars (or fewer than 150 distinct days) is also inconclusive, whatever the t.
