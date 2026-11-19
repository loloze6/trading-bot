---
brief: 016_grind-versus-jump-moves
source-idea: 016-01_up-grind-price-continuation.g1_big-moves-precede-rises
line: 7.b inconclusive
backtest: 016-01_up-grind-price-continuation.g1_big-moves-precede-rises_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's absolute 3-day return, the more the coin rises, only while that 3-day return is a fall, over the next 1 day.
Consequence: After a sharp 3-day fall a trader leans long for the following day, harder the deeper the fall, rather than holding a 3-day long after every move.
Why:
- F3: After a 3-day fall, the slope is strongest at the shortest horizon: t 5.36 over 24 bars (2,881 cases), falling to 2.92 at 48 bars and 2.27 at 72 bars. After a 3-day rise, the 24-bar slope is only t 0.52 (2,926 cases) and builds to 2.82 at 48 and 2.88 at 72 bars, so the plan's 3-day horizon mixes a fast rebound after falls with a slow drift after rises.
- F1: The rise after big moves comes almost entirely from the largest moves: the 72-bar excess return by forecast quintile is -0.44%, -0.22%, -0.18%, 0.00% and +0.84%, and the top decile earns +1.56% against -0.17% for the rest (Welch t 4.10, 568 top cases). Meanwhile the held position grows evenly from 0.06 to 0.46 across the quintiles, so the book is long through the middle quintiles, where the excess return is negative.
- F5: The move's size carries the signal, not its direction: the signed standardised 3-day return has a slope t of only 1.08 (5,539 cases), against 3.67 for the absolute size.
