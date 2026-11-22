---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue
line: 7.g patterns
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 48-hour move made on volume heavier than its mean over the preceding five days continues in the same direction over the next 48 hours, whatever the weekday. The heavier the last 48 hours' volume against the preceding five days, the larger the continuation.
Consequence: A move carried by unusually heavy volume is a reason to follow it for two days on any day of the week, not only after weekends.
Why:
- F3: A 48-hour move made on heavy volume continues over the next 48 hours on any day of the week, not only after weekends. On non-overlapping 23:00 anchors over all days, the top fifth of last-48-hour volume over the prior 120 hours gives a signed next-48-hour return minus drift of +0.64 % (t 3.29, 1593 cases), while the other four fifths range from −0.20 % to +0.09 % (|t| ≤ 1.28). Pooled over all days, the quintiles rise steadily from +0.05 % to +0.36 % (top t 2.69).
- F4: The heavy-volume continuation is strongest after the weekend. At Sunday 23:00 the top quarter of volume ratio gives +1.20 % (t 3.16, 572 cases), and the bottom quarter is reversed at −0.59 % (t −2.17). On Monday-to-Thursday anchors the top quarter gives only +0.24 % (t 1.54).
- F6: The book earns its money on Monday and Tuesday, as designed. Its mean daily return is +0.093 % on Mondays (t 2.67) and +0.076 % on Tuesdays (t 2.57), against −0.008 % to +0.015 % on the other days (Sunday −0.006 %, t −2.27).
