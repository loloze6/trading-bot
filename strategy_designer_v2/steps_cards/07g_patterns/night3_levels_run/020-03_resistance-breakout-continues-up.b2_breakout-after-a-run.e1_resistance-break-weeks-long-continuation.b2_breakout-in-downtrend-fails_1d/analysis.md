---
line: 7.g patterns
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.b2_breakout-in-downtrend-fails_1d
idea tested: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.b2_breakout-in-downtrend-fails
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3924 USD
---
## Findings
- **F1:** The book loses through the coin's drift rather than through its signal. Per case, the unusual move is +1.99 % over 20 days, but the normal drift in the short direction is -2.51 %, so the total move is -0.52 % against a cost of 0.19 %. Trades earned only in 2018 (+1.44 % per trade, 48 % won) and 2022 (+0.32 %, 46 % won), the only two years in which the coins' mean daily return was negative (-0.35 % and -0.18 %). In the six rising years trades lost between -0.68 % and -18.96 % each; the worst was 2020, with 13 % won while the coin rose 0.42 % a day.
- **F2:** The size of the forecast does not grade the trades. Mean net trade return by quartile of absolute entry forecast is -9.58 %, -3.70 %, -4.69 % and -6.57 % (223 trades each), and the verdict's rank correlation is only 0.026 over 413 cases.
- **F3:** The idea's situation is rare and points the right way, but not significantly. On a non-overlapping 20-day grid, 37 of 827 cells start on an active bar. Their unusual move is -5.66 % (price falls beyond drift, as the idea says), with t -1.46.
- **F4:** Five-day moves depend on the weekday of the starting close, but not clearly beyond chance. From Monday the unusual move is +1.43 % (t 3.04, 498 cases) and from Tuesday +1.40 % (t 2.71, 475). From Thursday it is -0.94 % (t -2.23) and from Sunday -1.18 % (t -2.18). With about 70 groupings examined, a top t near 3 does not stand out.
- **F5:** Grouping the bars by their past moves shows no graded pattern. By the last day's return, quintile 1 is followed by -1.48 % over 5 days (t -3.48), while quintile 0 gives +0.33 % and quintile 4 gives +1.01 % (t 1.95). By distance below the 60-day high, quintile 1 is followed by -5.19 % over 20 days (t -3.11) and quintile 3 by +4.07 % (t 2.57). Neither runs in order across quintiles.
- **F6:** Each window is short (119 to 123 days), so a 20-day horizon gives only about 6 independent cases per window and coin. Year-to-year swings of the book (F1) therefore weigh heavily.

## Ideas
- `020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.b2_breakout-in-downtrend-fails.g1_failed-breakout-in-downtrend` (from F1, F3): When a coin closes above a price where it turned down several times in the past 90 days, after a negative 30-day return and while its 180-day return is also negative, it falls over the next 20 days. The deeper that 180-day fall, the larger the decline.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
