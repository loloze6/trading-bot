---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d2_volatile-two-hour-overreaction-reverses
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d2_volatile-two-hour-overreaction-reverses_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour volatility is high, its large 2-hour move is followed by a move the opposite way over the next 24 hours. The larger the 2-hour move against its usual 2-hour move, the larger the move back.
Consequence: The tested overreaction is worth more held for a day than for 8 hours, so fewer, longer bets on the largest moves can clear the cost of a trade.
Why:
- F5: The tested 2-hour overreaction keeps reverting well past its 8-hour horizon. In high volatility, 2-hour moves of 3 to 4 usual moves give +38 bps over 8 hours (t 1.9, 579 cases) but +165 bps over 24 hours (t 3.0, 195 cases, strength 0.32). Moves beyond 4 give +57 bps over 8 hours (t 2.4) and +162 bps over 24 hours (t 2.3). Over 8 hours, only 2-hour moves above 2 usual moves (+28 to +57 bps) cover the 19 bps cost.
- F6: Most of the 8-hour cases are too small to pay. High-volatility 2-hour moves under one usual move make up 11188 of about 18200 cases and carry +3.7 bps (t 1.3), against a cost of 19 bps.
- F8: The book loses on the positions it holds long, not on its short ones. Trades held 8 hours or less net +0.61 % each (24937 trades). Trades held 16 to 48 hours net −1.92 % (9408 trades) and those beyond 48 hours net −5.05 % (2056 trades), for an overall net of −0.36 % per trade.
