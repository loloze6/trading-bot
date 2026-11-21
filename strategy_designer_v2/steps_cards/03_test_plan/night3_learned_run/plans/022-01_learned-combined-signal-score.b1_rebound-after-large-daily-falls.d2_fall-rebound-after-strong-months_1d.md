---
idea: 022-01_learned-combined-signal-score.b1_rebound-after-large-daily-falls.d2_fall-rebound-after-strong-months
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: a 1-day fall, large compared with 30-day volatility -> kept: the negated 1-day return in 30-day usual moves, clipped at 0.
- Comparison: the larger the size of the 30-day return, up or down -> replaced: the config cannot multiply the fall by the absolute 30-day return, and adding them is a different quantity.
- Outcome: a higher return over the next 1 day -> kept: a 1-bar horizon on daily bars.
- Verdict transfer: no: a sum or a regime gate on the 30-day move does not test "the more so" interaction, so neither result would transfer to the idea.
Reason: The forecast must grow with the product of the volatility-scaled 1-day fall and the absolute 30-day return. The config only takes weighted means of components, and none of them computes this product. Every input is in the coin's own closes.
