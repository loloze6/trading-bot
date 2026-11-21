---
idea: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.b1_breakout-continues-within-uptrend
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: e48527ec0eac
---
Fidelity:
- Situation: a close above a price where the coin turned down several times in the past 90 days -> adapted: `ResistanceBreakTouchCountComponent` (period 90) measures it, graded by touch count and by margin above the level.
- Comparison: only while the 30-day return is positive, and a larger 30-day return gives a larger rise -> replaced: a regime gate can keep only its sign, and no component multiplies the break reading by that return's size.
- Outcome: rises over the next 20 days, larger with more touches, margin and 30-day return -> kept: 20 bars held long.
- Verdict transfer: no: without the product, the 30-day return either drops out of the grading or adds a position when no break exists.
Reason: All three parts come from the coin's own closes and fit a graded long-only forecast, but the forecast must be the product of the break reading and the positive 30-day return. Strategy components can only be combined as a weighted mean, which gives a position without a break, and `score_product` only picks a regime.
