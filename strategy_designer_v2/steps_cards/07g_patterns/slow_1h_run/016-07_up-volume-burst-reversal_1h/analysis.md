---
line: 7.g patterns
backtest: 016-07_up-volume-burst-reversal_1h
idea tested: 016-07_up-volume-burst-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3428 USD
---
## Findings
- **F1:** Path efficiency predicts continuation after rises. Efficiency is the 72-hour net log move divided by the sum of absolute hourly log moves. Among risen bars on the 72-bar grid, excess forward 72-bar return rises steadily from the least efficient fifth (-0.0051, t -1.51, n 575) to the most efficient fifth (+0.0106, t 2.60, n 574).
- **F2:** The efficiency effect holds after controlling for move size. Regressing signed continuation on both efficiency rank and size rank, efficiency still adds continuation: coefficient 0.0182, t 2.21, n 5539 with a 72-hour look-back. With a 48-hour look-back it is 0.0224, t 2.80. Size itself leans toward reversal (coefficient -0.0181, t -2.26 at 48 hours).
- **F3:** The effect is consistent across coins and years but weak in most of them. On rises, the slope of continuation on efficiency is positive in all 6 coins (t from 0.37 for XMR to 2.78 for ZEC). Pooled over both directions, it is positive in 6 of 8 years (strongest 2020, t 2.51).
- **F4:** The efficiency effect is specific to the 3-day horizon and the shape of the move. It vanishes at a 1-day horizon (t 0.04, n 16814) and at a 5-day horizon (t -0.07, n 3250). On falls it reverses: on the down side all 6 coins have negative slopes, and the least efficient fallen fifth has excess -0.0096 (t -2.67, n 536).
- **F5:** The tested volume-concentration signal is weak and is beaten by efficiency. Among risen bars, excess return falls only from +0.0030 in the least concentrated fifth to -0.0041 in the most concentrated (t -1.33, n 574). The step-5 thirds gave t -1.10. Path efficiency on the same bars separates outcomes about twice as widely (F1).
- **F6:** The book's losses come from the timing of its trades, not from fees or from shorting a rising market. Gross gain per day before fees is negative on 5 of 6 coins (BTC -0.00121 against fees of 0.00068). The market's own rise accounts for only about a third of the per-bar loss (BTC -0.000019 of -0.000051). The book loses in 23 of 24 windows.

## Ideas
- `016-07_up-volume-burst-reversal.g1_efficient-rises-keep-rising` (from F1, F2, F3, F4, F5): When a coin has risen over the past 2 to 3 days, the more of its hourly movement over that period went in the direction of the rise (net move relative to the sum of absolute hourly moves), the more it rises over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
