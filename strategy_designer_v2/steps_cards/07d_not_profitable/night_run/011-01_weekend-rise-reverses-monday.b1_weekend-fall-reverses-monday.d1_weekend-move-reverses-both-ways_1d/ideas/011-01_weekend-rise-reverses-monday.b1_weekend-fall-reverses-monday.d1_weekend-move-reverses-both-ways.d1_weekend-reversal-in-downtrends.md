---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's return over the next 3 days (Monday to Wednesday) runs against its Sunday close-to-close move: after a weekend rise it falls and after a weekend fall it rises. The larger the weekend move relative to the coin's usual daily move, the larger the move back, only while the coin's 30-day return is negative.
Consequence: A trader would fade the weekend move for three days in falling markets and stand aside from fading weekend rises in rising markets, which is where the losing shorts and the deepest falls sit.
Why:
- F2: The move back does not end after one day; it keeps building through day 3. On the 1,817 Sunday cases, the reversal net of each coin's mean is 0.0059 (1 day) vs 0.0123 (3 days) in the largest-fall quintile, 0.0093 vs 0.0123 in the fourth quintile, and 0.0017 vs 0.0094 in the largest-rise quintile. The one-bar hold keeps less than half of it.
- F4: The losing side is a weekend rise while the coin's 30-day return is up. Those 526 cases show a 1-day reversal of 0.00098 (t 0.42) and a mean book gain of −0.0019. Weekend rises in 30-day down-trends reverse by 0.0101 (t 3.86, n 439) and falls in down-trends by 0.0085 (t 3.41, n 435).
- F6: The 60 worst book days average −9.2% for the book while the coin's own day averages +1.6%, and the coin rose on 58% of them. The deepest falls are shorts held into a continuing rise, which is what drags Calmar to 0.061.
- F1: The book holds a position only from the Sunday close to the Monday close, so it is flat six days in seven. Mean absolute position is 0.406 on Sundays against 0.000–0.0008 on every other weekday, and the mean gain is 0.001245 on Sunday bars and about 0 on all others. The book's mean daily return is therefore 5.6e-05, against 0.00119 for holding the coins and against the required 0.0005.
