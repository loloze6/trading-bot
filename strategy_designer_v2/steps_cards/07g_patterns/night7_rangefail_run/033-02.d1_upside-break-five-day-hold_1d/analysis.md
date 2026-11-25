---
line: 7.g patterns
backtest: 033-02.d1_upside-break-five-day-hold_1d
idea tested: 033-02.d1_upside-break-five-day-hold
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4142 USD
---
## Findings
- **F1:** The tested effect lives in calm markets. On 5-day non-overlapping cases, the slope of the unusual 5-day move on the close's position in its prior 20-day high-low range is 6.93 % per unit of range in calm markets (30-day swing at or below its median; 713 cases, correlation 0.217, t 5.92). In agitated markets it is only 2.16 % (709 cases, correlation 0.050, t 1.34).
- **F2:** In calm markets the drift is graded through the whole range and on both sides. The mean unusual 5-day move by range position is:
- **F3:** Over all profiles the range position grades the same way, from -2.11 % (t -1.15, 0–0.2) to +2.07 % (t 1.72, 0.8–1.0) and +5.10 % (t 2.14, 39 days) above the high. Breaks in the lowest-volatility third average +8.83 % (t 2.22, 18 days); breaks in the highest third average -2.46 % (t -1.01).
- **F4:** The book earns only in the first 5 days of a position.
- **F5:** The book's gain is lopsided. Its worst decile of days loses 0.76 % on days the coins fell 6.51 %, and its best decile gains 1.06 % on days the coins rose 6.18 %. Trade returns rise with the entry forecast, from +3.07 % (lowest third) to +9.81 % (highest third).
- **F6:** Other angles showed nothing that stands out against the number of looks:

## Ideas
- `033-02.d1.g1_calm-range-position-drift` (from F1, F2, F3): In a calm market, the higher a coin's daily close sits within its prior 20-day high-to-low range, the more it rises over the next 5 days, and the lower it sits, the more it falls, with closes above the 20-day high rising most.
- `033-02.d1.g2_calm-market-upside-break` (from F2, F3, F4): In a calm market, when a coin closes above its 20-day high, it rises over the next 5 days, and it rises more the further the close sits above that high.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
