---
line: 7.b inconclusive
backtest: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e1_breakout-continues-rising-week_4h
idea tested: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e1_breakout-continues-rising-week
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4219 USD
---
## Findings
- **F1:** The tested result is on the predicted side but small: +0.44 % unusual move per case over 12 days (t 0.85, 2249 cases, strength 0.017). That is 2.0 times the 0.22 % cost of a trade. The test already used all 19 coins and all four folds, so no more 4h data is available.
- **F2:** The effect is graded by the forecast and sits only in its upper part. By forecast quintile, the 12-day unusual move is −0.9 %, −1.4 %, −1.4 %, +1.9 % and +3.7 % (t −1.0 to +2.1). The top two quintiles together have a strength of 0.129 (t 3.13, 901 cases), and the slope check passes (t 3.96).
- **F3:** The effect is present only while the coin's 30-day return is positive. Within that regime, cases in the top two forecast quintiles gain +3.96 % (t 3.50, 436 cases), about 18 times the cost, and the other cases gain +1.18 % (t 1.29, 471). When the 30-day return is negative, cases lose −1.87 % (t −1.48, 191) and −2.13 % (t −2.56, 467).
- **F4:** The coin's longer trend carries the rest of the effect. By quintile of the 30-day return, the 12-day unusual move runs from −3.0 % (t −2.94) to +3.0 % (t 2.34). By quintile of price against its 20-day average, it runs from −3.6 % (t −4.11) to +5.6 % (t 2.67).
- **F5:** The market's yearly regime decides the sign. In 2022 cases lose −4.9 % (t −4.93) and in 2025 −4.8 % (t −4.77). In 2020, 2023 and 2024 they gain +4.9 %, +1.8 % and +3.2 % (t 3.29, 2.18, 3.20). This mix cancels the overall mean.
- **F6:** The plan's 12-day horizon is not where the move per case is clearest. Over 6 days the unusual move is +0.73 % (t 2.20, 2369 cases, strength 0.046), against +0.44 % (t 0.85) over 12 days. Over 6 days the top forecast quintile gains +2.1 % and the lowest +0.2 %.
- **F7:** No coin carries the effect on its own. Per-coin 12-day means range from −5.8 % (ONDO, t −1.76) to +2.9 % (SUI, t 0.92), and no coin reaches |t| 2.

## Ideas
- `019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e1_breakout-continues-rising-week.b1_breakout-continues-in-uptrend` (from F1, F2, F3, F4, F5): When a coin's four-hour bar closes above the high of its preceding two days, the coin rises more than usual over the next 12 days, and the larger its 7-day return before that bar, the larger the rise, only while the coin's 30-day return is positive.
- `019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e1_breakout-continues-rising-week.b2_breakout-continues-six-days` (from F1, F2, F6): When a coin's four-hour bar closes above the high of its preceding two days, the coin rises more than usual over the next 6 days, and the larger its 7-day return before that bar, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
