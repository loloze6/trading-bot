---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week
line: 7.d not profitable
backtest: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes above the highest high of a coin's preceding two-day stretch, the coin rises over the next three days. The rise is larger the further that close lies above the two-day high, measured against the coin's average four-hour range over the past 7 days, and larger still the quieter that 7-day range was compared with its 60-day average.
Consequence: A trader should size an upward four-hour breakout mainly by how far the close clears the two-day high, in units of the past week's typical range, and only secondarily by the quietness of the week.
Why:
- F1: The book fails on its size, not its sign: its mean daily return is 0.000496 against 0.0005 and its Calmar 0.71 against 0.75; per case the unusual move is +0.20 % over 3 days against a round trip of 0.19 % (1.1 times), so the edge the book bets on barely covers its cost.
- F2: The edge sits in how decisively the bar breaks out, not in how quiet the week was: with the close's distance above the prior 2-day high measured in units of the 7-day mean 4h range, the top fifth of breakouts has an unusual move of +1.31 % over 3 days (t 3.39, 590 cases), while the four lower fifths range from -0.77 % to +0.59 % (t -2.39 to 1.31).
- F3: The breakout bar's own return in units of the 7-day mean range grades the same way: the top fifth has +1.21 % (t 3.08, 590 cases) and the bottom fifth -0.54 % (t -1.79).
- F4: The quietness ratio the book sizes by grades weakly and not in order: by fifths the unusual move is +0.45 %, -0.08 %, -0.33 %, +0.55 % and +0.78 % (t of the top fifth 1.73, 311 cases).
- F5: The book's position follows the weak variable: it correlates 0.40 with the quietness ratio and only 0.12 with breakout strength, so its largest bets are not placed on the breakouts that carry the move.
- F6: Strong breakouts after a quiet week are the best cell: with both measures split into thirds, the strongest-and-quietest cell has an unusual move of +1.99 % (t 2.88, 184 cases), and the strongest-and-busiest cell +1.65 % (t 1.57, 158). The middle-strength thirds are all negative, from -0.49 % to -0.93 %.
