---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The heavier a coin's day volume relative to its own 30-day average volume on a day it closed higher, the lower its return over the next 3 days, only while its 30-day return is negative.
Consequence: A heavy-volume rally inside a falling month is a reason to refuse a long, or to lean short, over the next few days, more firmly the heavier the volume.
Why:
- F6: Heavy volume on an up day while the coin's 30-day return is negative is followed by a 3-day excess return of −0.024 (t=−3.9, n=166). The same heavy-volume long that the tested idea buys loses in this situation.
- F4: Heavy volume pays only on days the coin closed lower. On down days the top volume-ratio quintile (mean ratio 2.25) has a 3-day excess return of +0.0242 (t=4.5, n=397), and quintiles 0–3 sit between −0.001 and −0.005 with |t|<1.4. On up days the top quintile has −0.0033 (t=−0.8, n=460).
