---
line: 7.b inconclusive
backtest: 031-03_yearly-low-break-extends_1d
idea tested: 031-03_yearly-low-break-extends
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3599 USD
---
## Findings
- **F1:** Step 5's main measure is essentially zero: the mean short-side unusual 10-day move is +0.016 % with a day-clustered t of 0.007 over 77 cases on 57 days. My own first-case-per-cell reading gives the same answer: +0.21 %, t 0.08, 93 cases on 64 days, strength 0.04 of a usual move.
- **F2:** The depth of the break works against the idea. The deeper half of the cases has a mean unusual move 3.2 points below the shallower half (deeper minus shallower: -3.22 %). The Spearman correlation between the forecast (negative, more negative when deeper) and the short-side unusual move is +0.10, so deeper breaks are followed by less fall, not more.
- **F3:** The cases with the largest jumps in the forecast are the ones step 5's size uses (33 cases on 24 days). On those cases the coin rises against the short: the unusual move is -5.50 % per case over 10 days, t -1.96, -0.33 of a usual move of 14.49 %. The total move, drift included, is -7.13 %. That is near the reject bar, on the bounce side.
- **F4:** No other horizon shows a clear continuation. The mean short-side raw return after the first break in each cell is:
- **F5:** The effect is mixed across coins and years rather than held in one part of the data.

## Ideas
- `031-03.b1_deep-yearly-low-break-rebounds` (from F2, F3, F1): When a coin's daily close falls below the lowest close of the prior 365 days, it rises more than its usual drift over the next 10 days, and the further the close is below that old low, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
