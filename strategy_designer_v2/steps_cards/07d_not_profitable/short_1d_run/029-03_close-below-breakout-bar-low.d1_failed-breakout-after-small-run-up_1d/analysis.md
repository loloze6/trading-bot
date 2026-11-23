---
line: 7.d not profitable
backtest: 029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up_1d
idea tested: 029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3549 USD
---
## Findings
- **F1:** Most failed breakouts do not fall further. Recomputed from prices, a close below the breakout day's low within 3 days of a close above the prior 20-day high gives 361 cases with a short-side unusual 5-day move of −0.60 % (t −1.10). The broader close back below the old high gives −0.48 % (t −1.18, 619 cases) within 3 days, −0.64 % (t −1.73, 770 cases) within 5 days and −0.34 % (t −1.09, 1040 cases) within 10 days. The confirmed +2.83 % rests on 50 cases and does not hold for the situation at large.
- **F2:** The forecast fires on a small, unrepresentative share of failures, and even those carry little. It is nonzero on only 31 of the 361 recomputed failures (8.6 %), and those gained just +0.86 % (t 0.55). The 330 failures left at zero moved −0.74 % (t −1.27). The book held a position on 256 of about 17,524 coin-bars (1.5 %) and made 89 trades, or 0.00485 trades a day.
- **F3:** The book's trades lose after costs, and one coin carries most of the loss. Trades averaged −0.32 % net over 3.6 days, and only 37 % of them won. XMR summed −60.4 % over 22 trades and BTC −10.5 % over 25, while LTC (+15.4 %) and ZEC (+20.4 %) gained over few trades.
- **F4:** The idea's grading by the run-up is absent. The Spearman correlation between the 20-day run-up into the breakout day and the short-side move is 0.038. Run-up quintiles from the smallest (4.4 % average) to the largest (71 %) all lose, between −0.30 % and −1.23 %, with every |t| below 0.62.
- **F5:** Failures that arrive on a crash day bounce instead of falling, and the depth grading points the wrong way. The quintile with the largest one-day fall on the signal day (−10.8 % on average) is followed by a short-side move of −4.25 % (t −2.21, 73 cases), meaning the coin rose. The deepest-depth quintile (8.3 % under the breakout low) moved −2.71 % (t −1.51). The next fall quintiles (−6.2 % and −2.6 % that day) do continue: +0.91 % (t 1.12) and +1.11 % (t 1.16) over 5 days, and +3.27 % (t 2.45) and +2.72 % (t 1.94) over 10 days.
- **F6:** The losses cluster in one year. In 2020 the failures moved −2.94 % (t −2.33, 49 cases), the only year whose t lies beyond ±2. In 2025 they moved −2.73 % (t −0.93).

## Ideas
- `029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up.d1_slow-slip-failed-breakout-falls` (from F5, F1, F4): When a failed breakout above the prior 20-day high ends with a daily close below the low of the breakout day, the coin falls over the next 10 days. The closer the fall of that closing day stays to the coin's usual daily move, rather than a crash several times larger, the larger the fall that follows.
- `029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up.d2_crash-day-failure-rebounds` (from F5, F6, F2): When a coin closes back below the low of a breakout day above its prior 20-day high through a one-day fall far larger than its usual daily move, it rises over the next 5 days. The larger that day's fall against its usual daily move, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
