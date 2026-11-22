---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-03_uprun-volume-fade-depth-giveback
line: 7.d not profitable
backtest: 024-03_uprun-volume-fade-depth-giveback_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The more four-hour periods in a row a coin has closed higher, and the larger their summed gain relative to its typical four-hour move over the past 30 days, the more the coin rises over the next three days.
Consequence: Long, large up-runs would be a reason to buy rather than to short, and the exhaustion short would be refused exactly where it lost most.
Why:
- F3: Per case, the give-back is smaller than a trade's cost: the unusual 18-bar fall is +0.13 % (strength 0.014, t 1.15, 5709 cases) against a cost of 0.19 %. Against the coin's upward drift (-0.41 % in the short direction) the total move is -0.28 %, so no change of holding, sizing or threshold can make this signal pay.
- F4: The give-back is concentrated in mid-sized runs and reverses in the largest ones.
