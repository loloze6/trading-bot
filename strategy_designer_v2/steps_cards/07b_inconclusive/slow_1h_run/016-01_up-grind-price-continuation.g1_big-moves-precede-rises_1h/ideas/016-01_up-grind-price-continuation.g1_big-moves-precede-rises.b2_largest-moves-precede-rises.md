---
brief: 016_grind-versus-jump-moves
source-idea: 016-01_up-grind-price-continuation.g1_big-moves-precede-rises
line: 7.b inconclusive
backtest: 016-01_up-grind-price-continuation.g1_big-moves-precede-rises_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's absolute 3-day return, whether up or down, the more the coin rises over the next 3 days, and the rise grows faster than the move's size, so the largest moves are followed by far larger rises than moderate ones.
Consequence: A trader leans long mainly after the very largest 3-day moves and holds back after moderate ones, instead of scaling the long evenly with the move's size.
Why:
- F1: The rise after big moves comes almost entirely from the largest moves: the 72-bar excess return by forecast quintile is -0.44%, -0.22%, -0.18%, 0.00% and +0.84%, and the top decile earns +1.56% against -0.17% for the rest (Welch t 4.10, 568 top cases). Meanwhile the held position grows evenly from 0.06 to 0.46 across the quintiles, so the book is long through the middle quintiles, where the excess return is negative.
- F2: The book's timing part is negative on every coin, from -0.00024 (XRP) to -0.00076 (XMR) a day, while its gain from the market's own rise is +0.00015 to +0.00041 a day. Hourly, the timing sum by forecast quintile is -0.10, -0.01, +0.15, +0.73 and -0.06, while the market part grows from 0.29 to 2.36. So the positive slope (t 3.67, 5,683 cases) does not become timing profit for a book sized linearly on the forecast.
