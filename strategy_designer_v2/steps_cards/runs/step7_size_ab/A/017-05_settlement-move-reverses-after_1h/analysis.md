---
line: 7.d not profitable
backtest: 017-05_settlement-move-reverses-after_1h
idea tested: 017-05_settlement-move-reverses-after
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3692 USD
---
## Findings
- **F1:** The book loses because fees are about ten times its gross gain: pooled over all bars, the position's gain before costs averages +1.15e-5 per bar (about +2.8 bp of book per day), while fees average 1.08e-4 per bar (about 26 bp per day), which matches the failed mean daily return of -0.0023 and the Sharpe of -4.78.
- **F2:** Almost all of the fee comes from the open and close around each settlement, with 3.6 trades per day and 62,957 trades lasting 1 to 2 hours. Fees run 3.9e-4 to 5.0e-4 of book on the bars starting at 23, 7 and 15 UTC (entry) and at 1, 9 and 17 UTC (exit), and below 4e-6 on every other hour. The trade record puts the round trip at 0.10 % of notional (net -0.205 % against gross -0.105 % per trade).
- **F3:** The reversal is real but small next to that cost. On the 51,746 settlement bars, the 2-bar return signed by the forecast averages about +3.8 bp (1-bar about +1.9 bp), while the coins' mean absolute 2-bar move is 64 to 126 bp. That puts the edge near 3 % to 4 % of a usual move, roughly a third of a 10 bp round trip.
- **F4:** A larger pre-settlement move does not lift the reversal above cost. The signed 2-bar return by quintile of the standardised pre-move is -1.2, +6.1, +2.9, +7.0 and +4.2 bp, while the entry fee grows from 0.36 to 9.6 bp of book. The largest moves therefore pay the most fee for no larger reversal.
- **F5:** No settlement time and no coin clears the cost. The signed 2-bar return is +6.8 bp after the 00 UTC settlement (17,152 cases), +3.7 bp after 16 UTC and +0.8 bp after 08 UTC. By coin it runs from +1.9 bp (XRP) to +5.9 bp (ZEC), every one below the 10 bp round trip.
- **F6:** The trade record shows a gross loss of -0.105 % per trade (t = -16.0 over 62,957 trades), against a positive bar-level gross. The open and close around settlement therefore give back even the small bar-level edge before fees are counted.

## Ideas
- No ideas: The effect the book bets on is real but holds only a few basis points over the 2 hours after settlement, well under the 10 bp round-trip cost, and it does not grow enough with the pre-move, the settlement hour or the coin (F1, F3 to F5). No amended reading of the same clock-time reversal in these bars carries a move large enough to pay for trading it at every settlement.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
