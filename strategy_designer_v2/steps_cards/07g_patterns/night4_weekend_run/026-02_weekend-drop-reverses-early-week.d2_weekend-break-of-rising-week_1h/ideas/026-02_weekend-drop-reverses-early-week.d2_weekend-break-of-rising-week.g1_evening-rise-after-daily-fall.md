---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-02_weekend-drop-reverses-early-week.d2_weekend-break-of-rising-week
line: 7.g patterns
backtest: 026-02_weekend-drop-reverses-early-week.d2_weekend-break-of-rising-week_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Each coin rises over the 2 hours after the close of its 20:00 UTC bar, and the rise is larger the more the coin fell over its previous 24 hours and the higher its recent volatility.
Consequence: A trader can lean long into the late-UTC evening after a sharp 24-hour fall in a volatile coin, and should refuse evening shorts then.
Why:
- F1: The coin rises in the late evening in every coin: from the close of the 20:00 UTC bar over the next 2 hours it gains 8.1 to 10.5 bp per case, with a per-coin t between 2.7 (ZEC, 2372 cases) and 4.3 (BTC and ETH, 2628 each). Hours 21 and 22 on their own average +5.5 bp (t 6.9) and +4.4 bp (t 5.8) over all hours, the two strongest of the 24 hours by a wide margin.
- F2: This evening rise holds in 6 of 8 years, with t from 1.1 to 6.1; it is negative only in 2022 (−5.3 bp, t −1.7). It is positive on all seven weekdays (3.8 to 12.7 bp) and is weakest on Monday (t 1.2).
- F3: The evening rise is graded by the coin's own state. By the coin's volatility quartile it grows from 4.4 bp to 19.1 bp (t 2.9 to 6.2), with a strength of about 0.05 to 0.09 of a usual 2-hour move. After the coin's largest 24-hour falls (lowest quintile, past move −1.25 usual moves) it is 19.9 bp (t 6.3), against 1.3 to 10.8 bp in the other quintiles. The slope of the evening move in usual moves on the 24-hour return in usual moves is −0.021 (t −2.5, 15482 cases).
- F4: The cost of one trade is 0.19 %, and the evening move is below it on average (about 9 bp). It reaches about the cost (19 to 20 bp) only in the high-volatility and after-a-fall cases.
