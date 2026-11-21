---
line: 7.b inconclusive
backtest: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend.d1_false-break-while-month-falls_1d
idea tested: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend.d1_false-break-while-month-falls
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4292 USD
---
## Findings
- **F1:** The fade shows on the first day only: the short's excess fall over 1 day is +0.89 % (t 2.29, 106 cases, 58 % of them falling), against +0.21 % over 2 days (t 0.31), +0.35 % over 10 days (t 0.23) and +1.26 % over the plan's cut 10-day measure (t 0.97).
- **F2:** After the first day the coin does not keep falling back: from day 1 to day 10 the short's excess is −0.49 % (t −0.33, 106 cases), and over 20 days it is −1.27 % (t −0.63, 102 cases), so the plan's 10-day horizon spreads a one-day move across nine days of noise.
- **F3:** Ordinary falling-month bars fall more than these breaks do. On the 10-day grid of all bars with a negative 30-day return, the short's excess is +1.37 % (t 3.59, 1318 cases), against +0.35 % for the break cases. Over 10 days, a break of a repeatedly-held high in a falling month adds nothing to the month's own continuation, and the market's move drowns it.
- **F4:** On the first day the fall grows with the depth of the 30-day decline. The day-1 excess is +1.17 % for the deepest third (30-day return −10 % to −38 %, t 1.77, 23 cases), +1.15 % for the middle third (t 1.69, 22 cases) and +0.31 % for the shallowest third (−1.5 % to −4.5 %, t 0.39, 23 cases).
- **F5:** The 10-day result is mixed across periods and coins:
- **F6:** The size of the move per case is small next to the cost:

## Ideas
- `020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend.d1_false-break-while-month-falls.b1_one-day-fade-of-falling-month-breaks` (from F1, F2, F4, F6): When a coin closes above a price where it turned down several times in the past 90 days while its 30-day return is negative, it tends to fall back over the next day, and the deeper its 30-day decline, the larger that fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
