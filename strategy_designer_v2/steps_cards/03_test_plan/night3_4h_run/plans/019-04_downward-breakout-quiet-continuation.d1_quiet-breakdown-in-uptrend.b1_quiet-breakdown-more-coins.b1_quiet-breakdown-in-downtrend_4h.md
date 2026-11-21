---
idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins.b1_quiet-breakdown-in-downtrend
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 4h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 3d6ac1c822df
---
Fidelity:
- Situation: a 4h close below the lowest low of the preceding 12-bar (two-day) stretch, while the 180-bar (30-day) return is negative -> adapted: the break is graded as the close's depth below the prior 12-bar low (`DistanceFromHighComponent`, extreme "low", exclude_current 1, clip max 0), and the negative-month condition is a regime rule.
- Comparison: the stretch's narrowness against the 30-day average 4h bar range, where narrower means a larger fall -> replaced: no component multiplies a downward break by B/S, and a weighted sum cannot do it, so the size would come from adding the two parts rather than scaling one by the other.
- Outcome: the coin falls over the next three days (18 bars) -> kept.
- Verdict transfer: no: with an additive stand-in, the narrowness alone would set a short position without any break, so a result would not test the stated product.
Reason: The forecast needs a downward break's depth below the prior 12-bar low multiplied by how narrow that stretch is against the 180-bar mean bar range. The catalogue has this product only for upward breaks (`NarrowRangeBreakoutComponent`, `BreakoutInMeanRangesComponent`). The config can only add components by weight, and a score_product regime only gates a bar, it does not size the position. So the graded product cannot be built.
