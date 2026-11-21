---
idea: 020-03_resistance-breakout-continues-up.d1_held-breakout-keeps-rising
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: e48527ec0eac
---
Fidelity:
- Situation: a close above a price where the coin turned down several times in the past 90 days -> kept: `ResistanceBreakTouchCountComponent` (period 90) finds the crossed swing-high level and counts its turns.
- Comparison: only once the closes of the following 2 days stay above that level, larger the further above -> replaced: no component checks that each of the 2 later closes held above the level crossed 2 bars earlier.
- Outcome: the price keeps rising over the next 8 days -> kept: 8 bars on daily bars.
- Verdict transfer: no: without the hold condition, the test would mix breaks that held with breaks that slipped back, which the idea treats as opposite cases.
Reason: The idea needs a break 2 bars ago whose next 2 closes both stayed above the level. `ResistanceBreakTouchCountComponent` only checks close[t-cross_period] <= L < close[t]: it fires on the break bar itself and never checks close[t-1]. Differences of its `cross_period` 2 and 3 versions pick different levels and still leave close[t-1] unchecked, and no component or regime rule can read a lagged close against the level.
