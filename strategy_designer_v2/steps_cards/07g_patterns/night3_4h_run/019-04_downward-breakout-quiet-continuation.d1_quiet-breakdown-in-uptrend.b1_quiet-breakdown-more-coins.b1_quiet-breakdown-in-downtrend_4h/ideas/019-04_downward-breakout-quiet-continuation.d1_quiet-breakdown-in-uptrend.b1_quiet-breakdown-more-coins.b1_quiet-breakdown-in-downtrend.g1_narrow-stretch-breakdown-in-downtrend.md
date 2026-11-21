---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins.b1_quiet-breakdown-in-downtrend
line: 7.g patterns
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins.b1_quiet-breakdown-in-downtrend_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes below the lowest low of the preceding two days in a coin whose 30-day return is negative, the coin falls over the next three days. The narrower that two-day range is compared with the coin's 30-day average four-hour range, the larger the fall.
Consequence: Short downward breaks in a falling month in proportion to how narrow the prior two days were, without adding size for a deeper break.
Why:
- F1: The tested forecast is capped. 86 % of its active bars sit at -20 (median -20, 5th to 75th percentile all -20). The median split of the supporting check therefore put all 4087 cases in the smaller half and none in the larger. The idea's inconclusive verdict comes from this cap, not from a missing grading.
- F2: Down-breaks of the two-day range while the 30-day return is negative are graded by narrowness. The narrowest fifth of the stretch against the 30-day mean 4h range gives an unusual 3-day fall of +1.31 % (t 4.08, 588 cases). The widest fifth gives -0.95 % (t -2.35). Spearman rho is 0.107 (p 6e-9, 2937 cases).
- F3: The narrowness grading in F2 holds across the record.
- F4: The depth of the break grades the wrong way. The deepest third of down-breaks gives -0.66 % in the short direction over 3 days (t -2.73), against +0.28 % and +0.26 % for the shallower two thirds. The forecast's depth multiplier works against its narrowness term.
