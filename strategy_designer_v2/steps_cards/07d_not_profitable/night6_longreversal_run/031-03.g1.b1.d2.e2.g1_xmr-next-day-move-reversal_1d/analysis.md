---
line: 7.d confirmed, not profitable
backtest: 031-03.g1.b1.d2.e2.g1_xmr-next-day-move-reversal_1d
idea tested: 031-03.g1.b1.d2.e2.g1_xmr-next-day-move-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3667 USD
---
## Findings
- **F1:** The short side is what fails the Calmar: rebuilt with the backtest's costs, the book's short positions lose 0.016 % a day (Sharpe −0.32, deepest fall −52 %), and its long positions earn 0.097 % a day (Sharpe 1.05, deepest fall −33 %); the long side alone has a Calmar of 1.05, against 0.49 for the full book.
- **F2:** The book's deepest fall (−51 %, 255 days, window w22 to w24, year 2025) came while XMR rose 121 %. The short positions lost 28 % of the book in that fall and the long positions lost 16 %. Over all of 2025, the short positions summed to −25 % against +6.9 % for the long positions, while the coin gained 129 %.
- **F3:** The reversal is there only after falls. After z ≤ −2, the next day averages +1.54 % (70 days); after −2 < z ≤ −1, +1.11 % (237 days); both against the coin's mean of +0.107 %. After rises, it is weak or absent: −0.19 % after 1 < z ≤ 2 (269 days) and −0.51 % after z > 2 (66 days). Fading the rises earns a gross gain per bar of −0.013 % (t −0.13) for 1 < z ≤ 2 and +0.13 % (t 0.30) for z > 2.
- **F4:** After falls of z < −1, the rebound holds in every 60-day trend state, so no market state is the cause. The next day averages +1.77 % (t 2.35, 54 days) when the 60-day return is below −20 %, +0.66 % (t 1.38, 62 days) between −20 % and 0, +1.78 % (t 3.45, 38 days) between 0 and +20 %, and +1.35 % (t 1.59, 36 days) above +20 %. The long side's gain is positive in all four states, with t between 0.86 and 2.44.
- **F5:** About half the gross gain goes to fees: the position turns over 0.53 of the book per bar, about 0.082 % a bar in costs, against a gross gain of 0.165 % a bar. On small falls (−0.5 < z ≤ 0, 514 days), the long position earns only 0.008 % a bar gross (t 0.23), less than its trading cost.
- **F6:** Keeping only the long side and only the larger falls (z < −0.5) brings the deepest fall to −32 % and the Calmar to 0.81, with a Sharpe of 0.92. Holding the long side three days instead of one makes it worse (Calmar 0.48, deepest fall −54 %), so the effect lives in the next day.

## Ideas
- `031-03.g1.b1.d2.e2.g1.d1_xmr-next-day-fall-rebound` (from F1, F2, F3, F4, F5, F6): The larger XMR's one-day fall against its own 30-day daily volatility, the more its price rises back over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
