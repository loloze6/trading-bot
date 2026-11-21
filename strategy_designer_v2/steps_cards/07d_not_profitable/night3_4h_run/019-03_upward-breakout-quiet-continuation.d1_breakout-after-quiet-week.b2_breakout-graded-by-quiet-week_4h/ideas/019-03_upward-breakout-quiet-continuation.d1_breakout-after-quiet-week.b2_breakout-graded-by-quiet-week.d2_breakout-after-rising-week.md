---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week
line: 7.d not profitable
backtest: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes above the highest high of a coin's preceding two-day stretch, the coin rises over the next three days. The rise is larger the quieter the coin's average four-hour range over the past 7 days was compared with its average over the past 60 days, and larger the higher the coin's 7-day return at the breakout.
Consequence: A trader should give less weight to upward breakouts that come after a falling week, since these are the ones that fail inside long declines.
Why:
- F1: The book fails on its size, not its sign: its mean daily return is 0.000496 against 0.0005 and its Calmar 0.71 against 0.75; per case the unusual move is +0.20 % over 3 days against a round trip of 0.19 % (1.1 times), so the edge the book bets on barely covers its cost.
- F7: The deepest fall of the book is 24 % over 597 days, from w5 to w10, while holding the coins lost 57.5 %. In those windows even the strongest fifth of breakouts earned only +0.27 % (t 0.49, 181 cases) against +1.77 % (t 3.55, 409 cases) elsewhere, and the book held more then (mean position 0.52 to 0.66 against 0.47 to 0.56).
- F8: The coin's 7-day return before the breakout grades the move: breakouts in the lowest fifth of 7-day return (mean -8.5 %) have an unusual move of -0.77 % (t -2.49, 589 cases), and those in the highest fifth (mean +24 %) have +1.04 % (t 1.96).
