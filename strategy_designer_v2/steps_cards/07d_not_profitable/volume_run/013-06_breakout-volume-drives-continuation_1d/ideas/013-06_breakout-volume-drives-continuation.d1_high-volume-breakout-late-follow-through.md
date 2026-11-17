---
brief: 013_anchoring-to-recent-high
source-idea: 013-06_breakout-volume-drives-continuation
line: 7.d not profitable
backtest: 013-06_breakout-volume-drives-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above its prior 52-week high, the higher its volume on the breakout day relative to its own 90-day average, the larger its return over the next 30 days, and this return keeps building from the 10th to the 30th day after the breakout even on days when the coin is no longer at a new high.
Consequence: After a heavy-volume break of the 52-week high, a trader would keep the long for the following 30 days rather than drop it once new highs stop, since most of the extra gain comes late.
Why:
- F1: The book is almost never in the market: it holds a position on only 2.6% of bars and is flat on 85.5% of days. Its 346 trades last a mean 1.9 days (median 2). That is why the mean daily return is only 0.000152, against the 0.0005 needed.
- F2: The idea's payoff arrives across the whole 30 days, but the book holds only about the first week of it. Over 60 spaced breakouts, the high-volume half returned +0.224 over 30 days against +0.022 for the low half. Days 10–30 alone gave +0.068 against −0.024 (Welch t 1.52). Yet the book was in position on only 6.6 and 5.3 of those 31 days.
- F3: The short trades lose and only the trades that run on pay. The 171 trades of 1.5 days or less lose a mean −2.01% net. Trades of 3–7 days earn +15.5% (n=35) and the two trades of 7–15 days earn +46.4%.
