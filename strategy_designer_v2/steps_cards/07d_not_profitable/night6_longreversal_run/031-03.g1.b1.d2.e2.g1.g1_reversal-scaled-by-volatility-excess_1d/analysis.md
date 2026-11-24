---
line: 7.d confirmed, not profitable
backtest: 031-03.g1.b1.d2.e2.g1.g1_reversal-scaled-by-volatility-excess_1d
idea tested: 031-03.g1.b1.d2.e2.g1.g1_reversal-scaled-by-volatility-excess
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3891 USD
---
## Findings
- **F1:** The Calmar failed because of one deep fall. The book's deepest fall was −69.8 %, spread over 497 bars and 5 windows (w23 and w24 fell −64.5 % and −69.8 %). During it, XMR's summed daily returns were +1.38. The short positions lost 0.596 before fees and the long positions gained 0.233, while fees took 0.608.
- **F2:** The gain is on the long side only. After strong down days (forecast ≥ +8), XMR's next-day return averaged +1.03 % (t 5.06, 611 bars), against its normal drift of +0.107 % a day. Those bars made a gross 4.03 for 0.95 of fees. After strong up days (forecast ≤ −8), the next day averaged −0.18 % (t −1.04, 691 bars), so the shorts made a gross 0.77 and paid 1.02 in fees.
- **F3:** Weak forecasts (|forecast| < 8, 1595 bars) cost more than they earned. Their next-day return was −0.12 % (t −1.07); they made a gross 0.45, paid 1.20 in fees, and carried the largest fee share. The bottom three forecast quintiles each lost about −0.05 % a day after fees.
- **F4:** I re-ran the book in a simple simulation at the measured cost of 0.159 % per unit of turnover.
- **F5:** Being long is not the effect on its own. Any day long earns only the drift of +0.107 % against +1.03 % after strong down days. Weak bars in the top volatility-ratio tercile returned −0.002 % the next day, against +1.17 % for strong down days in the same tercile. Within the long side the move grows with volatility excess: +0.75 % in the low tercile, +1.17 % in the middle and +1.17 % in the high tercile. The condition therefore belongs to the idea's own grading.
- **F6:** On a non-overlapping 3-day grid, strong down days were followed by +1.48 % over 3 days (t 2.27, 186 cases), against +1.03 % over one day. Holding three days captures about 1.4 times the move for about a third of the turnover. After strong up days the 3-day return was −0.33 % (t −0.70, 229 cases).
- **F7:** A volatility filter alone does not repair the book. Trading only when the volatility ratio is above 1 reaches a Calmar of 0.43 with a deepest fall of −30 %, and adding |forecast| ≥ 8 gives 0.44.

## Ideas
- `031-03.g1.b1.d2.e2.g1.g1.d1_xmr-rebound-after-volatility-scaled-falls` (from F1, F2, F3, F4, F5): The larger XMR's one-day fall against its 30-day daily volatility, the more its price rises back over the next day, and this rebound grows with how far its 30-day volatility stands above its usual level over the past six months.
- `031-03.g1.b1.d2.e2.g1.g1.d2_three-day-rebound-after-falls` (from F2, F3, F6): The larger XMR's one-day fall against its 30-day daily volatility, the more its price rises back over the next three days, and this rebound grows with how far its 30-day volatility stands above its usual level over the past six months.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
