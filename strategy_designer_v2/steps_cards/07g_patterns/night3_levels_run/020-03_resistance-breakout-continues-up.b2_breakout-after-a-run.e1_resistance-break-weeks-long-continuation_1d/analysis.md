---
line: 7.g patterns
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation_1d
idea tested: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3802 USD
---
## Findings
- **F1:** The tested breakout adds nothing beyond the coin's drift: its 680 cases have an unusual 20-day move of +0.35 % (t 0.30, strength 0.004). Graded by the forecast's raw value, the breakout cases do not rise in order: the four quartiles give strength +0.011, -0.001, +0.095 and -0.127, and the top quartile is the worst (t -1.70).
- **F2:** The book is invested on 88 % of bars, and per coin its mean daily return tracks the coin's own (book against coin: BTC 0.0013 vs 0.0012, LTC 0.0003 vs 0.0007, ZEC 0.0013 vs 0.0016). Its Sharpe margin over holding (+0.12) comes from holding the coins' drift, not from timing breakouts.
- **F3:** A day whose return is large against the coin's 20-day volatility is followed by a rise over the next 5 days, measured on a 5-day grid with each coin's drift removed:
- **F4:** This top-quintile rise holds in both halves of the windows: +1.28 % (t 2.14, 276 cases) in w1-12 and +1.88 % (t 2.36, 294 cases) in w13-24. It is positive on 5 of 6 coins (BTC +1.6 %, ZEC +3.7 %, XRP +2.6 %; LTC -0.03 %).
- **F5:** Among positive days, the size of the day's move ranks with the next 5 days' excess return on all 6 coins (Spearman 0.03 to 0.09). The move per case, about 1.6 %, is roughly 8 times the backtest's 0.19 % round trip.
- **F6:** Over 3 days and 10 days the large-day effect is weak: the top decile gives +0.71 % (t 1.54) at 3 days and +2.21 % (t 1.28, 144 cases) at 10 days. The 5-day reading is the clearest, and it is one of about twenty angles examined.
- **F7:** The next day's excess return depends on the weekday:

## Ideas
- `020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.g1_large-up-day-continues` (from F3, F4, F5, F6): When a coin closes a day with a rise that is large against its own 20-day volatility, it tends to keep rising over the next 5 days. The larger that day's rise relative to its 20-day volatility, the larger the rise that follows.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
