---
idea: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 1f000a7ba652
---
Fidelity:
- Situation: the two hours from 21:00 to 23:00 UTC each day -> kept: a regime rule on the coming bar's hour (bars stamped 21:00 and 22:00).
- Comparison: the coin's hourly volatility over the past 7 days, a higher one meaning a larger rise -> kept: std of the last 168 hourly returns, sizing a graded long.
- Outcome: the coin rises over the 21:00 to 23:00 slot, more when volatility is higher -> kept: the 2-bar return from the 21:00 close to the 23:00 close.
- Verdict transfer: yes: the test holds long only in the slot, sized by the 7-day hourly volatility, so its slot gains confirm or reject both claims.
Forecast: Outside the slot the forecast is 0 (flat). On bars whose coming bar starts at 21:00 or 22:00 UTC, the forecast is long. Its size is the coin's hourly volatility: the standard deviation of the last 168 one-bar returns. That value is standardised against its own past 169 values, so it is about +10 when volatility is at its recent average. It grows towards +20 as volatility rises above that average and shrinks towards 0 as it falls below. It is never negative.
Config: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift_1h_config.json
Criterion:
- Horizon: 2 bars
- Main measure: Use one case per coin per day, taken at the bar stamped 20:00 (its close is 21:00). For each case, take the slot return close[22:00 bar] / close[20:00 bar] - 1. Subtract the coin's mean 2-bar return over all windows. Multiply the result by that bar's forecast / 10. The measure is the mean of this vol-sized excess slot gain over all cases (t of the mean), against holding the coin.
- Supporting check: Regress the excess slot return on the forecast at the 20:00 bar over the same cases. The slope must be positive with t ≥ 2: larger rises when volatility is higher.
- Confirm: The main mean is above 0 with t ≥ 2 and the supporting slope has t ≥ 2.
- Reject: The main mean has t ≤ -2, or the supporting slope has t ≤ -2.
- Inconclusive: Any other result counts as neither confirm nor reject: both t between -2 and 2, or one passes while the other is near zero. At least 500 slot cases are required; about 17,000 are expected across 6 coins and 24 windows.
