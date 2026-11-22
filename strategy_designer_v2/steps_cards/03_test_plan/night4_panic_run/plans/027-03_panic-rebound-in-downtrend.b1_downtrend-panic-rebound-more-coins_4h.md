---
idea: 027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins
brief: 027_panic-days-are-followed-by-a-premium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: a 24-hour stretch with a range several times its 30-day average and a hard fall -> adapted: "several times" and "hard" are made graded, as the close's drop below the prior 24-hour high counted in 30-day average bar ranges. The drop is large only when the stretch's range is large and the price fell through it; the bar-range unit cancels under standardise.
- Comparison: in coins whose 30-day return before the panic was negative; returns higher than usual -> kept: a regime on the 180-bar return ending 6 bars ago being below 0, and the outcome judged against holding the coin.
- Outcome: higher returns over the next 14 days, more so the more extreme the panic -> kept: 84-bar forward returns, with the long position growing with the drop.
- Verdict transfer: yes: the test measures the graded panic, only in coins with a negative prior 30-day return, against the coin's usual 14-day return.
Forecast: A regime rule uses VolatilityScaledReturnComponent (period 180, vol_period 20, lag 6). Its sign is the sign of the 30-day return ending just before the 24-hour stretch. When that return is below 0 the bar is in the `mean_reversion` regime; otherwise the bar is `unknown` and the forecast is flat. In `mean_reversion`, the forecast is BreakoutInMeanRangesComponent (period 6, base_period 180, side "below"). Its value is the prior 24-hour high minus the close, in units of the 30-day mean 4h bar range. It is: - standardised over 180 bars (min_periods 45); - then passed through signed_power with exponent 3 and pivot 20, the strongest graded dead zone, so ordinary small drops give nearly 0. The forecast is never negative. It is 0 when the close is at the prior 24-hour high, and it grows steeply with the depth of the panic drop, up to the +20 cap.
Config: 027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins_4h_config.json
Criterion:
- Horizon: 84 bars
- Main measure: A case is a bet: a rise of the forecast of at least 2 points, read once per cell of the non-overlapping 84-bar grid of each window. For each case, take the coin's 84-bar return from the signal bar minus the coin's mean 84-bar return over all windows. The measure is the mean of this excess over all cases and coins, with its t-statistic.
- Supporting check: The excess return of cases in the top third of the forecast at entry, minus that of the bottom third. This difference must be above 0.
- Confirm: The mean excess return is above 0 with t ≥ 2, over at least 30 cases, and the top-minus-bottom-third difference is above 0.
- Reject: The mean excess return is below 0 with t ≤ -2, over at least 30 cases.
- Inconclusive: Any of these gives no verdict: t between -2 and 2; a positive t ≥ 2 with a top-minus-bottom difference at or below 0; or fewer than 30 cases.
