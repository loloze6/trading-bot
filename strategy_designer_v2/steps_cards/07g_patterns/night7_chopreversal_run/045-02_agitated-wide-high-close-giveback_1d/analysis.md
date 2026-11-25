---
line: 7.g patterns
backtest: 045-02_agitated-wide-high-close-giveback_1d
idea tested: 045-02_agitated-wide-high-close-giveback
step 5: none
step 6: none
mode: one call
explorations: 2
cost: 0.2417 USD
---
## Findings
- **F1:** The record handed to this line is empty, so no pattern can be measured. Over two exploration rounds, `data` held the three tables (bars, trades, days), and each held 0 coins and 0 windows: 0 bars, 0 trades and 0 days.
- **F2:** Nothing was looked at, so nothing can count as a finding. That covers the forecast, the positions, the trades, the regimes, close location against the next day's return, wide days, large moves, weekdays, and the book's largest gains and losses. The empty record matches the missing verdict (step 5: none), the missing book check (step 6: none), and the size and cost of a trade, which were not recorded.

## Ideas
- No ideas: The backtest record for 045-02_agitated-wide-high-close-giveback reached this line with 0 coins, 0 windows, 0 bars, 0 trades and 0 days, so no pattern could be measured and no idea can rest on a finding. The backtest should be re-run or its record reloaded before this line reads it again.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
