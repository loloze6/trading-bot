---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d3_large-day-precedes-rise
line: 7.d not profitable
backtest: 022-01_learned-combined-signal-score.d3_large-day-precedes-rise_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's rise over its last day, measured against its usual daily move, the higher its return over the next 5 days, the more so the larger its 20-day return.
Consequence: Treat an unusually large up day in a coin already rising over 20 days as a reason to lean long for the next 5 days, and do not treat a large down day as one.
Why:
- F2: Only large up days carry the effect. On the non-overlapping 5-day grid, the excess 5-day return after the largest third of up days is +1.23 % (t 2.34, 453 cases). After the largest third of down days it is -0.01 % (t -0.03, 447 cases), and after mid-sized down days it is -0.61 % (t -1.20, 470 cases). Half the idea's situation, the down days, predicts no rise.
- F3: Mid-sized down days inside a falling 20-day trend are followed by a fall. Their excess 5-day return is -1.58 % (t -2.26, 242 cases). Large up days inside a rising 20-day trend are followed by a rise: +1.42 % (t 2.00, 301 cases), 7.5 times the 0.19 % cost of a round trip.
- F6: The idea as tested is too small to pay on its unusual move. That move is +0.09 % per case (strength 0.009), 0.5 times the 0.19 % cost of a round trip, so the book lives on the coin's drift (+0.59 %). That drift is what it gives back in a long bear stretch such as w12 to w14.
