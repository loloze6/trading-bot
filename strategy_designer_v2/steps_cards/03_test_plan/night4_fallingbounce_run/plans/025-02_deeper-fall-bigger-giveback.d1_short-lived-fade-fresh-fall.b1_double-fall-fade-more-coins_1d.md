---
idea: 025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall.b1_double-fall-fade-more-coins
brief: 025_bounces-fade-in-falling-markets
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 42de60c4e850
---
Fidelity:
- Situation: a one-day rise of several usual daily moves while the 90-day and 30-day returns are both negative -> adapted: both negative returns are kept as an on/off regime condition, and the rise of "several usual moves" is made graded, with a strong graded dead zone.
- Comparison: the larger the one-day rise in usual daily moves, the larger the fall -> kept.
- Outcome: the price falls over the next 2 days -> kept.
- Verdict transfer: yes: the test measures the same rise, under the same two conditions, against the same 2-day fall.
Forecast: The forecast is active only on bars where both the 90-bar and the 30-bar price change are negative. Elsewhere it is flat. On active bars it reads today's one-bar return divided by the standard deviation of the last 20 one-bar returns. This value is standardised over its past 60 values and clipped at 0, so only rises count. It then goes through signed_power with exponent 3 and pivot 20, which damps ordinary rises to about 0. It is then negated. The forecast is therefore zero or negative, and its size grows steeply with the size of the day's rise in usual moves. It is near 0 for small rises and reaches the maximum short (-20) for a rise of roughly 1.6 usual moves or more. It is never positive.
Config: 025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall.b1_double-fall-fade-more-coins_1d_config.json
Criterion:
- Horizon: 2 bars
- Main measure: A case is a short bet: the forecast falls by at least 2 points, read once per non-overlapping 2-bar grid cell of each window. For each case, take the coin's return from that bar's close over the next 2 bars, minus the coin's normal 2-bar drift over all its windows, in the short direction. Measure the mean of this value over all cases, with its t, before costs.
- Supporting check: Split the cases at the median of |forecast|. The mean short-direction excess return of the larger half minus that of the smaller half must be above 0.
- Confirm: The main measure's mean is positive with t >= 2, and the supporting check passes (difference > 0).
- Reject: The main measure's mean is negative with t <= -2: these bounces are followed by rises beyond the coin's drift.
- Inconclusive: Any t between -2 and 2. Also a main t >= 2 whose supporting check fails. Also fewer than 30 cases in total across coins and windows.
