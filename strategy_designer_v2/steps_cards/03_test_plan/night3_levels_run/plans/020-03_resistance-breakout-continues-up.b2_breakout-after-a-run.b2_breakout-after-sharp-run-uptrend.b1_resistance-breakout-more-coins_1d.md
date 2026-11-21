---
idea: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.b1_resistance-breakout-more-coins
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: e48527ec0eac
---
Fidelity:
- Situation: close above a price where the coin turned down several times in 90 days -> adapted: "several times" made graded, so the touch count times the close's margin above that level sizes the reading (ResistanceBreakTouchCount, 90 bars, break on this bar).
- Comparison: only while the 60-day return is positive; a larger 10-day return before the break means a larger rise -> kept: the 60-day return above 0 is a regime rule, and the 10-day return grades the size.
- Outcome: keeps rising over the next 5 days -> kept: the long bet is held 5 bars.
- Verdict transfer: yes: the break, the rising-quarter condition, the 10-day size and the 5-day rise are each measured as the idea states them.
Forecast: The forecast is active only on bars where the close has just crossed above a 90-day swing-high close level (touch count × percent margin above 0) and the 60-day return is positive. Off those bars it is 0. On an active bar it is the equal-weight mean of two parts: - the break reading (touch count × margin), standardised over 90 bars; - the 10-day return, standardised over 60 bars and clipped at 0. It is never negative. It grows with: - how often the level turned the price down; - how far the close sits above the level; - how sharp the 10-day run before the break was. Each bet is held 5 bars.
Config: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.b1_resistance-breakout-more-coins_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: For each case (a long bet: the forecast rises by at least 2 points, read once per 5-bar grid cell), take the coin's 5-bar return from the signal bar minus the coin's mean 5-bar return over all windows; test its mean with a t-test.
- Supporting check: The mean of this excess return weighted by the forecast exceeds its unweighted mean.
- Confirm: Mean excess return t ≥ 2 over at least 30 cases, and the supporting check passes.
- Reject: Mean excess return t ≤ -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2, fewer than 30 cases, or a confirming t with the supporting check failing.
