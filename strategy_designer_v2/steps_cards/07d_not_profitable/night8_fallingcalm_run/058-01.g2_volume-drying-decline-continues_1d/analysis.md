---
line: 7.d confirmed, not profitable
backtest: 058-01.g2_volume-drying-decline-continues_1d
idea tested: 058-01.g2_volume-drying-decline-continues
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4447 USD
---
## Findings
- **F1:** The book's deepest fall, -16.8% over 339 days in windows w16 to w18, came while it held shorts that had drifted away from the lows. In w16 to w18, in-position bars more than 5% above the coin's 30-day low lost a summed -0.95 over 127 bars (mean -0.74% a day). The 16 bars still near the low earned +0.015. Holding the coins rose a summed +0.91 over the same stretch.
- **F2:** Inside the idea's falling calm regime, signal cases near the 30-day low carry the effect and those that have bounced do not.
- **F3:** Being near the 30-day low is not an effect on its own, so it can repair the idea.
- **F4:** Near the low, the effect stays graded by the volume shrink. The stronger-forecast half earns +6.0% (t 3.39, 40 cases) against +1.6% (t 1.10, 39 cases) for the weaker half.
- **F5:** Keeping only the book's positions on bars within 5% of the 30-day low fixes both failing measures in the rebuilt gross book.
- **F6:** The book's losses come from shorts held after a bounce.
- **F7:** The size against cost is not the obstacle. The total move per case is +0.46% against a 0.19% trade cost, and near the low the total move is +3.1% per case. The gain is lost to positions kept on after the coin has bounced, not to fees.

## Ideas
- `058-01.g2.d1_volume-dry-up-at-the-lows` (from F1, F2, F3, F4, F5, F6): In a falling, calm market, the more a coin's volume over its last 30 days has shrunk against the 30 days before, and the closer its close still sits to its 30-day low, the more its 30-day fall carries on over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
