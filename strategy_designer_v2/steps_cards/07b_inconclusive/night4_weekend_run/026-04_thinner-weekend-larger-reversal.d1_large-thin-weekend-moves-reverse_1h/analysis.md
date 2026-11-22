---
line: 7.b inconclusive
backtest: 026-04_thinner-weekend-larger-reversal.d1_large-thin-weekend-moves-reverse_1h
idea tested: 026-04_thinner-weekend-larger-reversal.d1_large-thin-weekend-moves-reverse
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5633 USD
---
## Findings
- **F1:** The plan's cube forecast shows almost no grading. On the 2,084 recorded Sunday-close cases, the forecast's t against the 48-hour drift-removed return is 1.48 and its cube root's is 0.61, with a Spearman correlation of 0.035. Step 5's slope t is 0.45 and its size is -0.03 % per case (strength -0.001), so the result is effectively zero, and more cases of the same forecast would not lift it.
- **F2:** Thinness alone does grade the reversal, and only at Sunday's close. The 48-hour reversal regressed on log(weekday volume over weekend volume) has slope 0.0084 and t 3.02 on 2,099 cases. The thinnest quintile reverses +0.72 % (t 2.18) and the least thin -0.79 %, with top minus bottom t 2.76. On the other six weekday closes the same slope's t lies between -0.58 and 1.57, which is the weekend-only pattern the brief predicts.
- **F3:** The product the idea names works when built as log-thinness times the move's size in usual 48-hour moves (capped at 3): its t against the 48-hour reversal is 4.09. The plan's standardise-then-cube transform loses this. Thinness and move size are correlated at -0.41.
- **F4:** The effect is on one side only.
- **F5:** Move size alone does not grade the reversal, which undoes the idea's "large moves only" condition. The Sunday 48-hour reversal by |move| quintile is -0.61 %, -0.24 %, -0.08 %, +0.66 % and -0.38 %. Inside the thinnest quintile, the reversal does rise with move size across move-size terciles: +0.05 %, +1.12 %, +1.36 %.
- **F6:** The thinness effect holds across time and in most coins.
- **F7:** Where it shows, the move is large next to a trade's 0.19 % cost. The thinnest-quintile reversal after a weekend rise is 1.46 % over 48 hours, about 7.7 times the cost, and 2.55 % over 96 hours.

## Ideas
- `026-04_thinner-weekend-larger-reversal.d1_large-thin-weekend-moves-reverse.b1_thin-weekend-rises-fade` (from F2, F3, F4, F5, F7): The lower a coin's weekend volume is compared with its volume over the preceding five weekdays, the larger the share of its Saturday-Sunday move that is reversed over Monday and Tuesday, only after a weekend rise. The fall over the next 2 days grows with the product of the weekend's thinness and the rise's size in the coin's usual 48-hour moves.
- `026-04_thinner-weekend-larger-reversal.d1_large-thin-weekend-moves-reverse.b2_thin-weekend-rise-four-day-fade` (from F2, F4, F6, F7): The lower a coin's weekend volume is compared with its volume over the preceding five weekdays, the more its Saturday-Sunday rise is reversed, over the next 4 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
