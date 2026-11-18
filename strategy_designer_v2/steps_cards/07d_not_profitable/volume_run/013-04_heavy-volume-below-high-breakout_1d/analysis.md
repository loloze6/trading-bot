---
line: 7.d not profitable
backtest: 013-04_heavy-volume-below-high-breakout_1d
idea tested: 013-04_heavy-volume-below-high-breakout
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4539 USD
---
## Findings
- **F1:** The book is almost never in the market: it holds a position on only 1.38% of bars, across 152 entries with a median spell of 1 day (mean 1.56, max 5). Trades per bar are 0.0095 and the mean daily return is 5.9e-05, which explains why the size, trades and Calmar measures fail even though the bars it does hold gain 0.99% a day against 0.13% for all bars.
- **F2:** The book drops the break far too early: its position is lost as soon as the close slips back under the prior high, so it holds only 11.3% of the 30 days after each break. Over those 30 days the idea's own horizon pays, with a 30-day excess of +9.5% on 49 non-overlapping break cases (t 1.33) and a 6.4% excess on trending bars against -0.08% on the others.
- **F3:** The 30 days after a break pay as a whole. A unit position held on every one of those 1,531 days earns a mean 0.49% a day with an annualised Sharpe of 1.64, on 8.9% of all bars. The book's in-position days in that span earn 0.86% excess (t 2.03, n 237), and the days it sits out still earn 0.14% excess (t 1.01, n 1,869).
- **F4:** The post-break gain is front-loaded. Daily excess is 1.00% on the break day (t 1.92, n 152) and 0.88% over days 1–2 (t 2.13, n 285), then falls to between -0.19% and +0.18% over days 3–30. Measured from day 2 to day 30, the return is +8.9% on average but positive in only 47% of the 49 cases.
- **F5:** Heavy pre-break volume speeds the move up but does not carry it. After the heaviest-volume breaks (mean ratio 2.35), daily excess is 1.50% over days 0–2 and 0.83% over days 3–10, then -0.69% over days 11–29 (t -1.73). After middle-volume breaks (ratio 1.28), excess is still +0.61% over days 11–29 (t 2.01), and that tercile is the best over the whole 30 days (0.50%, t 2.44).
- **F6:** Holding the coin's 30 days after a break pays even when the price has fallen from its post-break peak. Daily excess is +0.47% on days 1–30 in the deepest drawdown quartile (mean -28% from the peak, t 1.26) and +0.47% near the peak (t 1.85). Falling back below the high therefore does not mark the move as over.

## Ideas
- `013-04_heavy-volume-below-high-breakout.d1_hold-the-whole-breakout-month` (from F1, F2, F3, F6): When a coin closes above its prior 52-week high, the heavier its volume over the preceding 10 days, relative to its own 90-day average, the larger its return over the next 30 days, and this return keeps building on the days when its close has slipped back below that prior high within those 30 days.
- `013-04_heavy-volume-below-high-breakout.d2_heavy-volume-breaks-run-fast` (from F4, F5): When a coin closes above its prior 52-week high, the heavier its volume over the preceding 10 days, relative to its own 90-day average, the larger its return over the next 10 days, with the move concentrated in the first days after the break.
- `013-04_heavy-volume-below-high-breakout.d3_freshest-breaks-pay-most` (from F4): The fewer days since a coin's close above its prior 52-week high, the larger its return over the next 2 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
