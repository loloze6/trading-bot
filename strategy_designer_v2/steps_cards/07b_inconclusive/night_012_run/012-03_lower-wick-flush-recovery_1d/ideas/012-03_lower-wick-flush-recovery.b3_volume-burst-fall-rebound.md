---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-03_lower-wick-flush-recovery
line: 7.b inconclusive
backtest: 012-03_lower-wick-flush-recovery_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Among bars that fall sharply, the larger the bar's volume relative to its prior 20-day mean, the larger the price rise over the next 3 days.
Consequence: The volume burst, not the wick, is what marks a sharp fall that tends to be retraced, so a trader leans into sharp falls in proportion to their volume burst.
Why:
- F5: The volume burst sets flush bars apart from other sharp falls over 3 days, but the wick does not. Sharp falls with a volume burst beat those without by +0.0168 in 3-day excess return (Welch t 2.00; n 163 vs 205). Among sharp falls without the burst, a close near the high predicts a weaker 3 days (slope t −2.99).
- F3: Over the next day, flush bars that close nearer their low rebound more. By quartile of close-near-low (1 − wick: 0.54, 0.74, 0.84, 0.94), the next-day excess return rises −0.013, −0.004, +0.010, +0.029 (about 41 bars each). Controlling for fall size and log volume ratio, that slope is +0.097 with t 2.78, while fall size has t −0.14.
