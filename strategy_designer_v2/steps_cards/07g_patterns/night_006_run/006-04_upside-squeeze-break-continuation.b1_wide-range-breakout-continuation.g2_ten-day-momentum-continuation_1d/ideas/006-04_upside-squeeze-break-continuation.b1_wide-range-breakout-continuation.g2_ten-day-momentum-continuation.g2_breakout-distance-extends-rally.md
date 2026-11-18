---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g2_ten-day-momentum-continuation
line: 7.g patterns
backtest: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g2_ten-day-momentum-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's close sits above the highest high of its prior 20 days, the more its price rises over the next 10 days.
Consequence: A trader would size breakout longs by how far price has cleared the prior 20-day top, not just by whether it broke out.
Why:
- F2: Among grid bars whose close sits above the prior 20-day high, the 10-day excess return is +0.064 on average (t=2.40, 86 cases), and it grows with the size of the break (slope 1.98, t=4.30).
- F3: Range position adds nothing once the 10-day return is known. In a joint regression of 10-day excess return, the 10-day return has t=3.31 and the position in the 20-day range has t=-0.19 (about 1,690 cases).
