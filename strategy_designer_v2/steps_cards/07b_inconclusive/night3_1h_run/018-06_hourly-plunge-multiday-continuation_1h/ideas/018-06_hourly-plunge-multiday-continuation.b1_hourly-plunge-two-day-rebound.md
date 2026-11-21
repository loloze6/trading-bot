---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation
line: 7.b inconclusive
backtest: 018-06_hourly-plunge-multiday-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, falls by a large multiple of its 30-day average absolute daily return, the price rises over the next 2 days by more than the coin's usual 2-day drift, and the larger the 24-hour drop in those multiples, the larger the rise.
Consequence: An hourly plunge of several daily moves is a reason to buy for the next two days rather than to short it.
Why:
- F2: The further fall is not graded by the size of the drop, and the largest drops are followed by a rise rather than a further fall. The Spearman of drop size against 120-hour strength is −0.001 (step 5: −0.014). Mean 120-hour strength by drop size:
- F7: The rise after the largest drops is strongest when the coin is in an uptrend. With a positive 30-day return, drops of 3 or more multiples give a short strength of −0.53 over 24 hours (t −2.65, n 27) and −0.51 over 48 hours (t −3.39, n 26). That is about half a usual 2-day move, many times the cost. Over all drops, the Spearman of drop size against 24-hour strength is −0.05: larger drops lean toward a larger rise.
- F1: The tested idea shows no effect at any horizon, so the inconclusive result does not come from testing at the wrong horizon. On the first bar per 120-hour cell where the 24-hour return reaches −1 multiple of its 30-day mean absolute daily return, the mean short strength is 0.025 over 48 hours (t 1.45, 3049 cases), 0.007 over 120 hours (t 0.40, 2990 cases) and 0.003 over 240 hours (t 0.16, 2850 cases). This matches step 5's 0.0007 (t 0.04, 3165 cases).
- F6: Even where the effect is not cancelled, it is far below the cost of a trade, consistent with findings F10 and F11. The unusual move is −0.02 % per case against a 0.19 % round-trip cost. The total move is −0.67 %, against the short, because of the coins' normal upward drift.
