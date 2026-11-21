---
idea: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.b2_breakout-in-downtrend-fails
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: e48527ec0eac
---
Fidelity:
- Situation: a close above a price where the coin turned down several times in the past 90 days -> adapted: "several times" becomes graded by the level's touch count times the close's margin above it (ResistanceBreakTouchCount, 90 bars, swing turns of closes).
- Comparison: after its 30-day return was negative, and the deeper that fall, the larger the decline -> kept: the 30-day return below 0 is the regime gate, and its depth grades the size.
- Outcome: falls back over the next 20 days -> kept: a short position held for 20 daily bars.
- Verdict transfer: yes: the forecast is short exactly on such breaks after a falling month, and its size grows with the fall's depth and the level's strength, so the 20-day result speaks to the idea.
Forecast: The forecast is active only on a bar whose close has just crossed above a 90-day swing-high close level (break reading above 0) while the 30-day return is negative. On all other bars it is 0. On an active bar it is the weighted mean of two parts, both always short: - the 30-day return, standardised over 60 bars (negative, larger in size the deeper the fall), weight 2; - the break reading, standardised over 90 bars and negated (larger in size the more touches the level had and the further the close clears it), weight 1. The forecast is negative, and grows in size with the depth of the fall and the strength of the break. Each bet is held 20 bars.
Config: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.b2_breakout-in-downtrend-fails_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: The mean unusual move per case, in the short direction. A case is each short bet, read once per 20-bar grid cell. Its unusual move is minus the coin's 20-bar return from the signal bar's close, after removing the coin's normal 20-bar drift over all windows. The mean is tested with the t of the mean over the cases, before costs.
- Supporting check: Over the cases, the rank correlation between the absolute entry forecast and the short-direction unusual move is above 0.
- Confirm: The mean short-direction unusual move has t ≥ 2 over at least 20 cases, and the supporting check passes (rank correlation > 0).
- Reject: The mean short-direction unusual move has t ≤ -2 over at least 20 cases: the price rises beyond its drift after such breaks.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is fewer than 20 cases. So is t ≥ 2 with a rank correlation of 0 or below.
