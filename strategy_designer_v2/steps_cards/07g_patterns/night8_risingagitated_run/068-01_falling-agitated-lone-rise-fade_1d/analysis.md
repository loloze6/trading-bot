---
line: 7.g patterns
backtest: 068-01_falling-agitated-lone-rise-fade_1d
idea tested: 068-01_falling-agitated-lone-rise-fade
step 5: none
step 6: none
mode: one call
explorations: 2
cost: 0.1870 USD
---
## Findings
- **F1:** The backtest's record holds no data to read: `data["bars"]`, `data["trades"]` and `data["days"]` are dicts with 0 coin-window entries each (round 2: 0 entries across all three tables), and the bars' column list is empty.
- **F2:** The verdict (step 5) and the book's check (step 6) are both "none", and neither the idea's size nor the cost of a trade was recorded, so nothing here can be checked against the forecast, the positions, the trades, the regimes or the bars.

## Ideas
- No ideas: The backtest record is empty (0 coin-window tables in bars, trades and days, and no verdict, check or size), so no pattern could be measured and no finding supports an idea; the backtest should be rerun before this line reads it again.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
