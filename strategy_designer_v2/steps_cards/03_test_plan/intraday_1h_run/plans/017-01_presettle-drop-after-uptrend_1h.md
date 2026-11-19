---
idea: 017-01_presettle-drop-after-uptrend
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a strong 3-day run-up, in the 2 hours before a funding settlement at 00:00, 08:00 or 16:00 UTC -> adapted: "strong" is made graded (a 72-bar rise, clipped at 0), and the 2 hours are held as a regime.
- Comparison: the stronger the 3-day rise, the larger the decline -> kept: the short position grows with the size of the rise.
- Outcome: the price falls over the 2 hours before settlement -> kept: the position is held on the 2 one-hour bars ending at settlement.
- Verdict transfer: yes: the test measures exactly whether the 2-hour pre-settlement return is negative and grows with the 3-day rise.
Forecast: A clock rule selects the 2 hours before each settlement. These are the coming bars stamped 22:00, 23:00, 06:00, 07:00, 14:00 and 15:00 UTC (HoursToSettlement 1 or 2). On those bars the forecast is the 72-bar percent price change, standardised against its own past 72 values (window 72, min_periods 20). Only rises are kept (clip at 0), and the sign is then flipped. The forecast is therefore 0 after a flat or falling 3 days and short after a rise, and the short grows with the size of the rise, up to -20. On every other bar it is 0, which means flat.
Config: 017-01_presettle-drop-after-uptrend_1h_config.json
Criterion:
- Horizon: 2 bars
- Main measure: The cases are settlement episodes, one per settlement. Each case starts at the bar stamped 21:00, 05:00 or 13:00 UTC with forecast < 0. On each case, take (-forecast/10) x (close[t+2]/close[t] - 1 minus the coin's mean 2-bar return over all its windows). Pool the cases across coins and test their mean with the ordinary t. A positive value means the short earns beyond holding.
- Supporting check: Among the same episodes, compute the mean excess 2-bar return of the top third by |forecast| minus that of the bottom third. This difference must be below 0.
- Confirm: The main-measure t is ≥ 2 and the supporting check's difference is below 0.
- Reject: The main-measure t is ≤ -2: the pre-settlement return rises with the 3-day run-up.
- Inconclusive: A t between -2 and 2 is inconclusive, and so is a t ≥ 2 when the check fails. At least 200 episodes with forecast < 0 are required, counted inside windows only.
