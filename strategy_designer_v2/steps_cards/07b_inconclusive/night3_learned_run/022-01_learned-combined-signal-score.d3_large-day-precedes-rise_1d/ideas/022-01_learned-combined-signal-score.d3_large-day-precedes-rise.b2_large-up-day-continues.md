---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d3_large-day-precedes-rise
line: 7.b inconclusive
backtest: 022-01_learned-combined-signal-score.d3_large-day-precedes-rise_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's rise over its last day, the higher its return over the next 5 days.
Consequence: Treat an unusually large up day as a reason to lean long the coin for the following 5 days, more the larger the day.
Why:
- F4: The two sides of the idea differ.
- F5: The size of the move is large enough against cost only in the strongest cases.
- F6: The grading holds on both sides separately at 5 days. Within up days, the slope of the 5-day excess return on the size of the move is +0.0022 per forecast point (t 2.51, 1557 cases). Within down days it is +0.0020 (t 2.55, 1718 cases). The test's one-sided thirds split diluted this, because the bottom third was mostly near-still days whose returns are noisy.
