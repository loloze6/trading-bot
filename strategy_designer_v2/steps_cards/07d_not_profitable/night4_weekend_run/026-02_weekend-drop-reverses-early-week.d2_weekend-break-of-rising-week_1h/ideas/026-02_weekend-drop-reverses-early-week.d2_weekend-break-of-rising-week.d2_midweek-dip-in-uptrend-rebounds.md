---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-02_weekend-drop-reverses-early-week.d2_weekend-break-of-rising-week
line: 7.d not profitable
backtest: 026-02_weekend-drop-reverses-early-week.d2_weekend-break-of-rising-week_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin falls over two days during the week after rising over the previous five days, it rises over the next two days. The rise is larger the larger the preceding five-day rise was, measured in the coin's usual moves.
Consequence: A trader should buy a midweek two-day dip in a strongly rising coin rather than short it.
Why:
- F5: The same situation on weekday closes does not continue but reverses. It gives a short-side 48-hour move of -0.06 % (t -0.54, 3538 cases), against +0.44 % (t 1.36, 533) on Sundays. On weekdays, the quartile with the largest prior rise gives -0.72 % (t -3.19, 885), and the quartile with the largest two-day fall gives -0.66 % (t -2.93, 885): the coin rebounds.
