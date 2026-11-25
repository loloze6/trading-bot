---
idea: 042-01_low-close-next-day-rebound
brief: 042_close-location-reverses-next-day
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 18d3cc56dd45
---
Fidelity:
- Situation: where the day's close sits within that day's high-low range -> kept: the close's distance below the day's high, as a share of the range, graded.
- Comparison: the coin's next-day rise against its normal drift, stronger nearer the low -> kept: judged against holding, with drift removed, graded by close location.
- Outcome: the coin rises over the next day -> kept: return over the next 1 bar on daily bars.
- Verdict transfer: yes: the forecast is the idea's close location itself, held one day, so a graded payoff confirms it and a reversed one rejects it.
Forecast: The forecast uses CloseLocationInRangeComponent with reference "high", which reads (high - close) / (high - low): 0 when the close is at the day's high and 1 when it is at the low. It is standardised over the 60 days before the bar, so its usual size is +10. A standardised BuyAndHold, negated to the constant -10, is added at equal weight. The forecast is therefore (x - 10) / 2, where x is the standardised close location. It is positive (long) when the close sits nearer the low than this coin's usual close. It is negative (short) when the close sits nearer the high. It is zero at the usual location. It grows linearly with how low the close sits, to about +5 at the low and about -5 at the high. It is ungated and acts in every market profile.
Config: 042-01_low-close-next-day-rebound_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The pooled least-squares slope of the next-day return on the bar's forecast, over all coins and windows. The next-day return is close[t+1]/close[t] - 1 minus the coin's mean daily return over all windows. The forecast is rebuilt from the post_pipeline_values. The slope's t uses standard errors clustered by day.
- Supporting check: The drift-removed next-day return of the top forecast quintile minus that of the bottom quintile, pooled over coins, must be above 0.
- Confirm: The slope's t is 2 or more, and the top-minus-bottom quintile difference is above 0.
- Reject: The slope's t is -2 or less.
- Inconclusive: A slope t between -2 and 2 is inconclusive. So is a t of 2 or more with a top-minus-bottom difference at or below 0. The test needs at least 1000 distinct days with recorded forecasts across the coins, else it is inconclusive.
