---
idea: 018-05_hourly-plunge-loss-before-close
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a coin's 24-hour return, read at an hourly close, first reaches several times its usual size on the downside -> adapted: the "first reaches several times" threshold becomes a graded short that grows with the 24-hour fall and is held while the fall lasts.
- Comparison: the coin's 30-day average absolute daily return -> kept: the 24-hour return is standardised by the mean absolute 24-hour return over the previous 720 hourly bars.
- Outcome: the price keeps falling from that hour to the same day's daily close, more after larger drops -> kept: measured from the signal bar's close to the close of that UTC day's last hourly bar.
- Verdict transfer: yes: the measure reads the idea's own situation, its own 30-day yardstick and its own end point, the same day's close.
Forecast: The forecast starts from the 24-hour price change in percent (PriceEvolutionComponent, period 24). It is standardised over the previous 720 hourly values (30 days), so the 30-day average absolute 24-hour move reads 10. A fall of twice that average reads -20, the cap. The positive side is clipped to 0, so the forecast is short only. A cubic dead zone (signed_power, exponent 3, pivot 20) keeps ordinary falls near flat: - a fall of 1x the average gives -2.5; - 1.5x gives -8.4; - 2x or more gives -20. The forecast is zero on rises and near zero on ordinary falls. It grows in size smoothly as the drop gets larger in multiples, and saturates at 2x (the cap of standardise and of the forecast).
Config: 018-05_hourly-plunge-loss-before-close_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: The cases are, per coin and per UTC day, the first bar on which the forecast falls to -2 or below from above -2. For each case, take the coin's return from that bar's close to the close of the same UTC day's last bar, in the short direction. Subtract the coin's mean hourly return over all windows, times the hours remaining. Then compute the one-group t of the mean, pooled over coins and windows, before costs.
- Supporting check: The mean of this excess short return for cases with forecast at -10 or below, minus that for cases between -10 and -2, is above 0.
- Confirm: Confirmed when the mean excess short return has t >= 2 over at least 30 cases and the supporting difference is above 0.
- Reject: Rejected when the mean excess short return has t <= -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2, or a confirming t with a supporting difference at or below 0, is inconclusive. So is any result with fewer than 30 cases in total.
