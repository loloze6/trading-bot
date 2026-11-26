---
line: 7.g patterns
backtest: 061-01.g1.d1.d2.d1_calm-outsized-rise-continues_1d
idea tested: 061-01.g1.d1.d2.d1_calm-outsized-rise-continues
step 5: none
step 6: none
mode: one call
explorations: 2
cost: 0.2591 USD
---
## Findings
- **F1:** The backtest record I was given is empty: `data["bars"]`, `data["days"]` and `data["trades"]` each hold 0 coins and 0 windows (0 rows in all three tables, checked in two rounds), and steps 5 and 6 gave no verdict ("none"). So I measured no forecast, position, trade, regime or bar pattern, and the idea's size against the 0.19 % cost of a trade could not be measured either.

## Ideas
- No ideas: The backtest record has no bars, days or trades (0 coins, 0 windows), so I found no pattern to support an idea; the backtest of 061-01.g1.d1.d2.d1 should be re-run or its record re-attached before this line reads it again.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
