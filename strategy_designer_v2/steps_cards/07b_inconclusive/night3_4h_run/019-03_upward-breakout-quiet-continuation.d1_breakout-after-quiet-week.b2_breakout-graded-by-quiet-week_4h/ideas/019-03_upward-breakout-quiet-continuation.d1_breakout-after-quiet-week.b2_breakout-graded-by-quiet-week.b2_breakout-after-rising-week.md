---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week
line: 7.b inconclusive
backtest: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes above the highest high of a coin's preceding two-day stretch, the coin rises over the next three days, only while its 5-day return is positive. The rise is larger the quieter the coin's average four-hour range over the past 7 days was compared with its average over the past 60 days.
Consequence: A trader should take an upward four-hour breakout only when the coin has risen over the past five days, sized by how quiet the preceding week was, and refuse breakouts that come after a falling week.
Why:
- F2: The breakout's direction depends on the coin's recent path. Breakouts made while the coin's 5-day return was positive were followed by +0.74 % unusual moves over 3 days (t 3.72, 2149 cases). Breakouts after a falling 5 days were followed by −1.16 % (t −4.50, 792 cases). The two signs cancel in the tested pool.
- F3: The same split holds on the 10-day return. Breakouts after a rising 10 days gave +0.54 % (t 2.52, 1816 cases) and those after a falling 10 days gave −0.42 % (t −1.68, 995 cases), a difference of +0.96 % (Welch t 2.92). Only the lowest 10-day-return quintile is negative (−1.01 % at 3 days, t −2.64; −1.85 % at 6 days, t −4.17). The other four quintiles all sit at +0.36 to +0.62 % over 3 days.
- F4: Inside rising stretches the effect is spread rather than held by one coin. After a rising 10 days, BTC gave +0.53 %, ETH +0.59 %, XRP +2.10 % (t 2.54) and ZEC +0.77 %, while LTC (−0.50 %) and XMR (−0.02 %) did not.
- F6: The quietness grading is weak and not monotone.
