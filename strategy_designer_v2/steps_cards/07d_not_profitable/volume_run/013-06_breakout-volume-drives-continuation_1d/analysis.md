---
line: 7.d not profitable
backtest: 013-06_breakout-volume-drives-continuation_1d
idea tested: 013-06_breakout-volume-drives-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3051 USD
---
## Findings
- **F1:** The book is almost never in the market: it holds a position on only 2.6% of bars and is flat on 85.5% of days. Its 346 trades last a mean 1.9 days (median 2). That is why the mean daily return is only 0.000152, against the 0.0005 needed.
- **F2:** The idea's payoff arrives across the whole 30 days, but the book holds only about the first week of it. Over 60 spaced breakouts, the high-volume half returned +0.224 over 30 days against +0.022 for the low half. Days 10–30 alone gave +0.068 against −0.024 (Welch t 1.52). Yet the book was in position on only 6.6 and 5.3 of those 31 days.
- **F3:** The short trades lose and only the trades that run on pay. The 171 trades of 1.5 days or less lose a mean −2.01% net. Trades of 3–7 days earn +15.5% (n=35) and the two trades of 7–15 days earn +46.4%.
- **F4:** The 30-day follow-through grows sharply with breakout volume. New-high bars in the top forecast quartile (forecast 20) returned +0.305 over 30 days against −0.008 in the bottom quartile. Breakouts in the top raw volume-ratio tercile (mean ratio 5.76) returned +0.424, against about +0.10 in the other two terciles.
- **F5:** The book's falls are just the coin's own falls on the few days it is held, not a long losing state. The 15 worst book days averaged −9.4% while the coin fell −10.0%, and 7 of them were BTC. The deepest fall, −7.5% from w21 to w22, spanned 146 days but held only 19 losing days summing −0.98%. So Calmar fails mostly because the yearly return is small, not because the falls are deep.

## Ideas
- `013-06_breakout-volume-drives-continuation.d1_high-volume-breakout-late-follow-through` (from F1, F2, F3): When a coin closes above its prior 52-week high, the higher its volume on the breakout day relative to its own 90-day average, the larger its return over the next 30 days, and this return keeps building from the 10th to the 30th day after the breakout even on days when the coin is no longer at a new high.
- `013-06_breakout-volume-drives-continuation.d2_extreme-volume-breakout-continuation` (from F2, F4): When a coin closes above its prior 52-week high, the larger its breakout-day volume relative to its own 90-day average, the larger its return from 10 to 30 days after that breakout day, rising more than in step with the volume ratio.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
