---
line: 7.d confirmed, not profitable
backtest: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b1_settlement-reversal-more-coins_1h
idea tested: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b1_settlement-reversal-more-coins
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4786 USD
---
## Findings
- **F1:** The move back after settlement is short-lived, and the 8-hour hold throws it away. On settlement bars where the 2-hour move runs against the 24-hour trend, the drift-adjusted return in the trend's direction is +0.033 % after 1 h (t 6.2), +0.062 % after 2 h (t 8.5) and +0.041 % after 4 h (t 4.2). By 8 h it falls to +0.009 % (t 0.68), and by 16 h it is −0.084 % (t −4.1); there are 44,575 cases.
- **F2:** The book loses even before fees. It made 68,462 trades with a median length of 8 h, averaging −0.14 % gross and −0.24 % net, against a cost of 0.22 % per trade. It is in a position on 86 % of coin-days and makes 1.83 trades a day, so it pays the full cost on every case for a captured move of about +0.01 %. The result is a Sharpe of −0.92 and a yearly return of −16.1 %.
- **F3:** The settlement clock carries the effect, and it scales with the size of the pre-move. At 2 h, counter-trend cases at settlement earn +0.062 % against +0.015 % at non-settlement 4-hourly bars (47,404 cases).
- **F4:** The strongest case of the situation clears the cost of a trade. In the top 5 % of settlement cases by pre-move size × 24-hour trend strength (2,175 cases), the return in the trend's direction is +0.21 % at 2 h (t 4.2) and +0.27 % at 3 h (t 4.8). It drops to +0.16 % at 4 h and +0.11 % at 8 h (t 1.1). The 3-hour figure is about 1.2 times the 0.22 % cost, whereas the all-case 8-hour move is about 0.04 times it.
- **F5:** With an 8-hour hold, the trend's strength alone does not grade the move. Across trend-strength quintiles the 8-hour returns are +0.039, −0.004, −0.023, −0.061 and +0.082 %, which is not monotonic. Pre-move-size quintiles at 8 h rise only at the top (+0.099 %, t 2.6).
- **F6:** The effect is uneven across the three settlements. In the top pre-move decile at 2 h, the return is +0.24 % at 00 UTC (t 2.9, 623 cases), +0.12 % at 16 UTC (t 2.2, 1,260 cases) and −0.10 % at 08 UTC (t −1.1, 660 cases).
- **F7:** Without the counter-trend condition the move back is weaker. Reverting a with-trend pre-move in the top decile at settlement gives −0.046 % at 1 h and −0.010 % at 2 h (8,139 cases). The 24-hour trend condition is part of the effect, not decoration.

## Ideas
- `017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b1_settlement-reversal-more-coins.d1_strong-settlement-reversal-3-hours` (from F1, F2, F4, F7): The return over the 3 hours after each funding settlement time runs opposite to the return over the 2 hours before it when that pre-move runs against the coin's 24-hour trend. The larger the 2-hour pre-move and the stronger the 24-hour trend together, the larger the move back.
- `017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b1_settlement-reversal-more-coins.d2_pre-move-sized-settlement-reversal` (from F1, F3, F5): The return over the 2 hours after each funding settlement time runs opposite to the return over the 2 hours before it when that pre-move runs against the coin's 24-hour trend. The larger the 2-hour pre-move relative to the coin's usual hourly move, the larger the move back.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
