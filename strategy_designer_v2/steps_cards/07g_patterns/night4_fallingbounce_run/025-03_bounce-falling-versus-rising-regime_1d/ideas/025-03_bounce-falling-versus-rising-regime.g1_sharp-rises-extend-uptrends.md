---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-03_bounce-falling-versus-rising-regime
line: 7.g patterns
backtest: 025-03_bounce-falling-versus-rising-regime_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin whose 90-day return is positive, the larger the day's rise measured in usual daily moves of its last 20 days, the higher the coin's return over the next 5 days.
Consequence: A sharp rise in a rising coin is a reason to buy for the following days rather than to fade it, and more so the sharper the rise.
Why:
- F1: In coins whose 90-day return is 0 or above, the 5-day excess return after an up day grows with the rise's size in usual 20-day moves: +2.18 % (t 2.25, 149 grid cases) for 1 to 2 moves, +3.67 % (t 2.32, 43) for 2 to 3, and +7.28 % (t 1.85, 27) above 3. The slope of the 5-day excess return on the rise over all up days is +0.0138 per usual move (t 3.08, 751 cases).
- F2: These rising-market rises of more than one usual move have a strength of 0.267 of the coin's usual 5-day move (t 3.64, 219 cases), about 2.8 % per case, roughly 15 times the 0.19 % cost of a trade. They are positive in all six coins (t from 0.38 for LTC to 2.21 for ZEC) and in 7 of 8 years (only 2022 is negative, with 6 cases).
- F3: The tested fade in falling markets (90-day return below 0) does not show, which is what sinks the book:
