---
idea: 018-06_hourly-plunge-multiday-continuation
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the 24-hour return, read at an hourly close, first reaches several times its 30-day average on the downside -> adapted: the "several times" threshold becomes a graded size, and "first reaches" becomes "while it holds".
- Comparison: the coin's 30-day average absolute daily return -> kept: the 24-bar return is divided by the mean absolute 24-bar return over the past 720 bars.
- Outcome: the price keeps falling over the next 5 days, by more than the coin's usual 5-day move, and falls further after larger drops -> kept: a short bet held 120 bars, measured against the coin's 120-bar drift and usual move.
- Verdict transfer: yes: the forecast is the idea's own multiple of the daily move, short only, held for its 5-day horizon.
Forecast: The forecast starts from the 24-bar percent return (PriceEvolutionComponent, period 24). This is divided by the mean absolute 24-bar return over the 720 bars (30 days) before the bar, times 10, capped at -20 to +20. The result is the drop in multiples of the 30-day average daily move, times 10. Only the downside is kept (clip at 0 from above), so a rise gives 0. A signed_power with exponent 3 and pivot 20 is the strongest graded dead zone the guide allows. It keeps the forecast near 0 for ordinary days: 1 multiple gives -1.25 and 1.5 multiples gives about -8.4. Two multiples or more gives -20, which is a 200 % short. The forecast is never positive. It grows more negative as the 24-hour drop grows in multiples, and it saturates at 2 multiples because of the engine's ±20 cap. Note on settings: the standardise window of 720 bars is the idea's own 30 days. This is above the guide's usual 500-bar convention but within what the validator accepts. min_periods is the guide's maximum of 120.
Config: 018-06_hourly-plunge-multiday-continuation_1h_config.json
Criterion:
- Horizon: 120 bars
- Main measure: The cases are the forecast's short bets: a fall of at least 2 points, read once per non-overlapping 120-bar grid cell of each window. For each case, take the coin's 120-bar return from the signal bar's close and subtract the coin's normal 120-bar drift (pooled over all windows). Negate it so the short side is positive, and divide by the coin's usual 120-bar move (the standard deviation). This gives each case's strength. The measure is the ordinary t of the mean strength over all coins' cases, before costs.
- Supporting check: The Spearman rank correlation between each case's |forecast| at the signal bar and its strength is above 0.
- Confirm: The mean strength is positive with t ≥ 2 over at least 30 cases, and the rank correlation is above 0.
- Reject: The mean strength is negative with t ≤ -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2, a confirming t with a rank correlation of 0 or below, or fewer than 30 cases in total.
