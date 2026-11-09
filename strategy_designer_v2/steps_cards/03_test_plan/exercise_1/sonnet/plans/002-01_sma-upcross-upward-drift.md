---
idea: 002-01_sma-upcross-upward-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Config: 002-01_sma-upcross-upward-drift_config.json
Confirm: Forecast-weighted returns (forecast at bar close times the next bar's return) are positive, and cumulative gains rise with the size of the positive forecast: the top tercile of positive forecasts (strongest uptrend spread) is followed by higher mean next-bar and next-10-bar returns than the bottom tercile, and than the coin's unconditional average (buy-and-hold). Judged before costs.
Reject: Mean returns after large positive forecasts are no higher than the coin's unconditional mean, or are lower (reversal), or the strategy's gross return does not beat holding the coin and shows no rise in gains with forecast size.
Deviation: "After the cross" becomes "while the 50-day SMA is above the 200-day SMA, scaled by the size of the spread". The position is held at all times the spread is positive, not only after the cross event, and a negative spread gives a short position, which the idea (upside only) did not state. The test measures trend persistence across the whole spread, not just the bars right after the crossing. Price-crosses-average is not tested. The 50/200 periods come from convention and not from the brief.
