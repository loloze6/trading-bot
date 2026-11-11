---
idea: 003-07_quiet-hours-moves-revert
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a sharp price move in quiet hours or weekends, on low volume -> adapted: a sharp one-day move on a day whose volume is below its 20-day mean; quiet hours cannot be seen in daily bars.
- Comparison: none -> kept
- Outcome: the move is partly reversed once busier volume returns -> adapted: "once volume returns" becomes the next daily bar's return against the move.
- Verdict transfer: yes: the idea's working condition is low volume, which the test keeps; a reversal after thin-volume sharp days confirms it, and continuation rejects it.
Forecast: The forecast is active only on bars whose volume is below its 20-day mean. The detector checks this with a veto: the constant +10 passed through `volume_filter`, period 20. On every other bar the forecast is 0. On an active bar, the forecast is minus that day's percent close-to-close move (`PriceEvolutionComponent`, period 1), standardised against its past 60 daily values. It then goes through `signed_power` with exponent 3 and pivot 20, the strongest graded dead zone the guide allows. Small moves give almost no position. A move of average size gives about 2.5. A move twice the average size gives the full 20. The forecast is positive (long) after a thin-volume drop, negative (short) after a thin-volume rise, and grows with the cube of the move's size.
Config: 003-07_quiet-hours-moves-revert_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: The t-statistic of the slope from regressing the next bar's coin return on the forecast, over active bars. The coin return is taken minus its mean daily return in the same window, so the market's own drift is not credited. Windows are pooled, and each bar is counted once.
- Supporting check: Over the 20% of active bars with the largest |forecast|, the mean of sign(forecast) × the next bar's return, minus the window's mean daily return. A reversal makes this positive.
- Confirm: Slope t ≥ 2, with the supporting check's mean positive.
- Reject: Slope t ≤ -2, meaning thin-volume sharp moves carry on the next day.
- Inconclusive: Any t between -2 and 2, or fewer than 40 active bars with |forecast| ≥ 2 across the six windows.
