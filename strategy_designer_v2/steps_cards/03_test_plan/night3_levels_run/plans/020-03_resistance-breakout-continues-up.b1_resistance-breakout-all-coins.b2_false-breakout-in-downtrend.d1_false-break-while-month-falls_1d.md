---
idea: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend.d1_false-break-while-month-falls
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: e48527ec0eac
---
Fidelity:
- Situation: a close above a price where the coin turned down several times in the past 90 days, while its 30-day return is negative -> kept: regime rules require a fresh close above a swing-high level, at least 3 turns near the highest such turn below the close, and a negative 30-day return.
- Comparison: a deeper 30-day decline against a shallower one -> kept: the short forecast grows with the depth of the 30-day decline.
- Outcome: it falls back over the next 10 days, only while its 30-day return is still negative, and most when it stays deeply negative -> kept: each bet is held 10 bars, and the measure counts each case's fall only up to the first day the 30-day return turns positive.
- Verdict transfer: yes: the test builds the break, the touch count, the falling month, the depth grading and the 10-day fade cut at a positive month, so its result carries to the idea.
Forecast: The forecast is active only on bars where all three of these hold: - the close has just crossed above a swing-high close level of the past 90 days (`ResistanceBreakTouchCountComponent`, period 90, side 2, band 2 %, cross_period 1, above 0); - at least 3 swing highs of the past 90 days sit within 2 % of the highest turn below the close (`SwingHighClusterCountComponent`, level "below", pivot "high", count, bar t excluded); - the 30-day return is negative. On those bars the forecast is the 30-day return, standardised over its past 60 values and clipped at 0. It is a short whose size grows with the depth of the decline: near 0 for a month just below flat, about -10 for a usual decline, down to -20 for a deep one. On every other bar it is 0 (flat). It is never positive.
Config: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend.d1_false-break-while-month-falls_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: A case is each short bet (a fall of the forecast of at least 2 points), counted once per 10-bar grid cell. For each case, take the short's return from the signal bar's close. Count it day by day over the next 10 days, and stop at the first day the 30-day return (recomputed from the closes) is at or above 0. Subtract the coin's normal daily drift over the same days, so the market's own move is not credited. The measure is the t of the mean of this excess fall over all cases, before costs.
- Supporting check: Split the cases at the median of their 30-day return on the signal bar. The deeper half's mean excess fall minus the shallower half's must be above 0.
- Confirm: The idea is confirmed when the mean excess fall is positive with t >= 2 and the deeper-minus-shallower difference is above 0.
- Reject: The idea is rejected when the mean excess fall is negative with t <= -2: the coin rises after these breaks more than its drift.
- Inconclusive: Any t between -2 and 2 is inconclusive, and so is t >= 2 with a failed depth check. A test needs at least 30 cases over all coins and windows; with fewer it is inconclusive.
