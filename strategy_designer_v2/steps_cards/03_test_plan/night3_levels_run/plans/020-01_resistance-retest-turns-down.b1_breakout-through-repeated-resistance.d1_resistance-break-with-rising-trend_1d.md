---
idea: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.d1_resistance-break-with-rising-trend
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: e48527ec0eac
---
Fidelity:
- Situation: a close above a 90-day level where price turned down several times, after closing below it the day before -> adapted: `ResistanceBreakTouchCountComponent` (period 90, cross_period 1) grades the close-through by the close's margin above the level.
- Comparison: a larger rise with more past turns at the level, and more so the higher the 20-day return up to that close -> replaced: the touch count is kept, but no component multiplies it by the 20-day return.
- Outcome: the price rises over the next 10 days -> kept: 10 bars on 1d bars, long only.
- Verdict transfer: no: without the break-times-20-day-return interaction, a test would not show whether the rise grows with the prior 20-day rise or vanishes after a fall.
Reason: The forecast must multiply the resistance-break reading by the 20-day return up to the break. Weighted means only add components, and regimes and score-product only gate, so they cannot make this graded product. A sum would hold positions on 20-day rises with no break, and a 20-day-rise regime would make the return's grading on/off.
