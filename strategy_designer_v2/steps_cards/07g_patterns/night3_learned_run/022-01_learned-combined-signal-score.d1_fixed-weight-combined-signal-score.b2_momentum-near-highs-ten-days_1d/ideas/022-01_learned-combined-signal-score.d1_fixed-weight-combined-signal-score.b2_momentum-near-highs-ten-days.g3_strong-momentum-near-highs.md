---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b2_momentum-near-highs-ten-days
line: 7.g patterns
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b2_momentum-near-highs-ten-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 28-day return plus its closeness to its 90-day high, the higher its return over the next 10 days, by more the further both sit above their usual levels.
Consequence: A trader would take a long position only when four-week momentum and nearness to the three-month high are both strong, growing it with their strength, rather than shorting weak coins.
Why:
- F4: The forecast's edge is concentrated in its top fifth: +2.04 % unusual 10-day move (t 2.0), against −0.41 % to +0.33 % in the middle three fifths and −1.26 % in the bottom fifth (t −1.8, 342 cases per fifth). The same shape appears for momentum alone (top +2.04 %) and for nearness alone (top +2.03 %).
- F5: The book earns on its long side only. Positions held long earn +0.082 % per bar before costs and short positions −0.007 %, although the book is short 49 % of the bars and long 49 %.
- F3: The two components carry the same information rather than independent errors. Alone, the 28-day momentum has t 2.4 and the nearness to the 90-day high has t 2.6. Together in one regression they fall to t 0.96 and t 1.39 (1,691 cases), so the combination adds little over the better single effect.
