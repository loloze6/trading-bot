---
idea: 028-03_low-volume-up-fade.b1_quiet-up-hour-fade-wider
brief: 028_volume-confirmed-hourly-moves-continue
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: an hour whose rise is far above its typical hourly move over the past 30 days -> kept: the 1-bar return divided by the mean absolute 1-bar return over 720 bars, rises only, graded with a strong dead zone.
- Comparison: that hour's volume stays near its 30-day average hourly volume -> kept: a regime on the hour's volume over its 720-bar mean, between 0.67 and 1.5 by convention.
- Outcome: price gives back part of the rise over the next 2 to 6 hours, more after larger rises -> kept: a short sized by the rise and held 6 bars.
- Verdict transfer: yes: the test bets exactly on a fade after large rises on ordinary volume, sized by the rise, over the idea's horizon.
Forecast: The forecast is computed only on hours whose volume is 0.67 to 1.5 times its 720-bar mean; on all other hours it is 0. On those hours it starts from the hour's return measured in units of the 30-day mean absolute hourly return. This value is standardised over its past 500 values (min_periods 120) and clipped at 0, so only rises count. It is then passed through signed_power with exponent 3 and pivot 20, which keeps ordinary moves near 0, and negated. The result is a short that is near zero for typical hours, grows steeply with the size of the rise and is capped at -20. The forecast is never positive.
Config: 028-03_low-volume-up-fade.b1_quiet-up-hour-fade-wider_1h_config.json
Criterion:
- Horizon: 6 bars
- Main measure: The cases are short bets (the forecast falls by at least 2 points), read once per 6-bar grid cell of each window. For each case, take the unusual move: minus the coin's 6-bar return from the signal bar's close, minus the coin's normal 6-bar drift. Measure its mean over all cases, pooled over coins and windows, with the ordinary t of the mean.
- Supporting check: Across the cases, regress the unusual move on the size of the forecast at the signal bar. The slope must be above 0: a larger rise gives a larger giveback.
- Confirm: The mean unusual move is above 0 with t ≥ 2 over at least 30 cases, and the supporting slope is above 0.
- Reject: The mean unusual move is below 0 with t ≤ -2 over at least 30 cases, meaning large rises on ordinary volume carry on rather than fade.
- Inconclusive: Inconclusive if t is between -2 and 2, or if the main measure confirms but the slope is not above 0. Fewer than 30 cases is also inconclusive, whatever the t.
