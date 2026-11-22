---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue
line: 7.d not profitable
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's Saturday-Sunday move made on higher volume than its mean over the preceding five weekdays continues in the same direction over the next 5 days, the more so the larger the move and the heavier the weekend volume against the weekdays, only while the weekend move extends the coin's move over the preceding five weekdays, and the more so the larger that weekday move in the same direction.
Consequence: A heavy-volume weekend move that extends the week's trend is a reason to follow it through the whole next week, and one that goes against the week is a reason to stay out.
Why:
- F1: The book's gain is too thin because it is mostly flat. It holds a position on only 6–18 % of bars depending on the coin, is flat on 52 % of days, and holds a mean absolute allocation of 0.56 at the cases. Its mean daily return is 0.024 % against the 0.05 % required, while its mean on the days it is in a position is 0.050 %.
- F2: The weekend move keeps extending well past the 48-hour hold. On the 463 Sunday-23:00 cases the signed return is +1.15 % at 48 h (t 2.65) and +2.13 % at 120 h (t 3.44). The increment from 48 to 120 h is +0.93 % (t 1.96, 453 cases). On the volume-gated weekends the unusual move doubles from +1.14 % at 48 h (t 2.49, 432 cases) to +2.37 % at 120 h (t 3.74, 422 cases).
- F3: The continuation lives almost entirely in weekends that extend the preceding weekdays' move. Among gated weekends whose move has the same sign as the prior five weekdays' move, the unusual 120 h move is +3.83 % (t 4.71, 257 cases), against +0.10 % (t 0.10, 165 cases) when the weekend goes against the week. Across all weekends the same split is +0.89 % (t 2.46, 1086 cases) against −0.09 % (t −0.29, 1133 cases).
- F4: The Friday move points the same way. Cases where the Friday before the weekend moved in the weekend's direction gain +1.72 % over 48 h (t 2.83, 270 cases), against +0.20 % (t 0.31, 180 cases) otherwise.
- F7: The Calmar failure comes from a deep fall late in the folds and from losing tails. The book's deepest fall is −14.2 % over 288 days, from w22 to w24, where five of six coins' trades lost (ZEC −63 %, XMR −38 %, XRP −30 % summed). XMR loses overall (−128 % summed over 135 trades, worst trade −62 %). The worst 1 % of trades lose more than 24.5 %, and the 10 worst days sum to −0.27 against a total of +0.70.
