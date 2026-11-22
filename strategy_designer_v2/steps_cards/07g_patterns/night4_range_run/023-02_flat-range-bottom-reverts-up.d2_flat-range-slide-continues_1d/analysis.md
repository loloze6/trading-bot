---
line: 7.g patterns
backtest: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues_1d
idea tested: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3805 USD
---
## Findings
- **F1:** The book loses because it is short into sharp rallies. On its worst 1 % of coin-days the book lost -7.57 % while the coin rose +10.40 %, and on its best 1 % it gained +7.26 % while the coin fell -9.88 %. Its trades lost on average after fees on every coin, from -1.03 % (ZEC, 501 trades) to -2.34 % (XRP, 501 trades).
- **F2:** The book's trades do worse the larger the 10-day fall they enter on, the reverse of the idea. Trades in the most negative entry-forecast quartile lost -2.39 % on average (727 trades, median -2.37 %), against -0.71 % in the least negative quartile (727 trades). This matches the step-5 slope t of -0.02 on 1085 grid bars.
- **F3:** In flat coins (net move ≤ half the 30-day range), the next-5-day excess return is not graded by depth below the middle or by the size of the 10-day fall.
- **F4:** A coin's one-day move scaled by its 20-day daily volatility predicts the next day's excess return, graded on the down side.
- **F5:** Other patterns did not survive averaging by date, so they are not findings.

## Ideas
- `023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.g1_outsized-down-day-rebounds` (from F4, F1, F2): The larger a coin's one-day fall relative to its usual daily move over the past 20 days, the more that coin rises over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
