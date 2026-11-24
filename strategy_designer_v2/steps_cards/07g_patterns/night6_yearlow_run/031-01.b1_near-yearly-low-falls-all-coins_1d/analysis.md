---
line: 7.g patterns
backtest: 031-01.b1_near-yearly-low-falls-all-coins_1d
idea tested: 031-01.b1_near-yearly-low-falls-all-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4621 USD
---
## Findings
- **F1:** Nearness to the 365-day low does not grade the next 20 days. Excess 20-day return by quintile of raw proximity, from farthest to nearest, was -0.93 %, -1.10 %, +2.49 %, +0.05 % and -0.51 % (299 cases each). The day-pooled Spearman correlation was 0.08 over 147 days. At the low itself (proximity ≥ 0.9) the excess return was -4.1 % over 20 days (t -0.72, 31 cases on 15 days) and +1.5 % over 5 days (t 0.79, 95 cases on 50 days).
- **F2:** The tested forecast's only negative bucket is its capped end. The top quintile of |forecast| (-17.1 to -20) had a mean excess of -3.26 % (t -2.6 with cases not pooled by day). The next quintile had +2.47 %, so the relation is not graded. The size check could not tell the unusual move from zero: -1.56 %, t -0.93 over 343 days.
- **F3:** Saturday stands out among weekdays as a calendar condition, but it is on/off rather than graded.
- **F4:** Reversal after a large down day is weak and unstable.
- **F5:** None of these situations grades the 20-day excess return:
- **F6:** The book is essentially a short on the market's moves, with no timing.

## Ideas
- No ideas: The one pattern that stands out against the many angles looked at is the Saturday rise (F3), and it is an on/off calendar condition with no graded situation. Every graded situation examined (nearness to the yearly low, large down days, past returns, volatility, distance from recent lows) was non-monotone or could not be told from chance (F1, F2, F4, F5).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
