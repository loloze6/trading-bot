---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-02_weekend-drop-reverses-early-week.d2_weekend-break-of-rising-week
line: 7.d not profitable
backtest: 026-02_weekend-drop-reverses-early-week.d2_weekend-break-of-rising-week_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin falls over the weekend after rising over the previous five days, it keeps falling over Monday and Tuesday. The fall is larger the smaller the weekend's fall is next to the preceding five-day rise, each measured in the coin's usual moves.
Consequence: A trader should short a shallow weekend dip in a strongly rising week as the start of a pullback. A deep weekend drop has already done the move and should be left alone.
Why:
- F2: Inside the active Sunday cases, the move is graded by the weekend fall, inversely to what the forecast is built on. Cases are split into terciles by weekend return. The smallest falls are followed by a short-side 48-hour move of +1.45 % (t 2.80, 178 cases). The middle tercile gives +0.52 % (t 1.06). The largest falls give -0.48 % (t -0.73).
- F3: On all qualifying Sundays, the ratio of the weekend fall to the prior rise (in usual moves) grades the move in the same way. The lowest quartile, a small fall against a large rise, gives a short-side 48-hour move of +1.46 % (t 2.32, 134 cases). The second quartile gives +1.16 % (t 1.66). The two highest quartiles give -0.71 % and -0.17 %.
- F4: The forecast's own size, the prior five-day rise, barely grades the outcome, yet it drives the position. Across prior-rise terciles the short-side 48-hour moves are +0.49 %, +0.08 % and +0.92 % (t 1.02, 0.13, 1.56). Over the same terciles the mean absolute allocation rises from 0.17 to 0.53 to 0.66. The book is therefore largest on cases whose size is not where the move is.
- F1: The book cannot reach the gain asked of it at this frequency. It trades only on the Sunday close and holds for 48 hours, so it is exposed on 17 % of days (0.170), with 912 trades in all (0.050 a day). Each case earns a total move of only +0.49 % at a mean absolute allocation of about 0.45, against a cost of 0.19 % per trade. The mean daily return is 4.7e-05, against the 0.0005 required.
