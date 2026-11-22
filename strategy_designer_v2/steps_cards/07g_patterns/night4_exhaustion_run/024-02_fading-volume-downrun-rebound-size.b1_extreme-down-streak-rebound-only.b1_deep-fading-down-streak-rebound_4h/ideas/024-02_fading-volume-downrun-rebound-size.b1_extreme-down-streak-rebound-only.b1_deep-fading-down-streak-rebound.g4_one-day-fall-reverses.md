---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only.b1_deep-fading-down-streak-rebound
line: 7.g patterns
backtest: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only.b1_deep-fading-down-streak-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The larger a coin's fall over its past day, counted in its usual one-day move over the last 30 days, the larger its rise over the next three days.
Consequence: A trader buys sharp one-day falls in proportion to their depth, expecting part of them to be retraced within three days.
Why:
- F4: The last day's return, in usual moves, reverses over the next 3 days: rank correlation −0.053 (p 0.0001, 5292 cases); the bottom fifth (the sharpest one-day falls) is followed by +0.79 % excess (t 2.76, 1059 cases); in the joint regression it keeps t −3.37, while the 3-day past return carries the opposite sign (t +3.54).
- F5: The tested idea moves almost nothing: +0.05 % unusual move per case over 3 days (strength 0.007, t 0.37, 4039 cases), against a cost of 0.19 % per trade; the book's 1 % worst days (−13.2 %) and best days (+14.8 %) match the coin's own moves on those days (−13.0 % and +14.7 %), so its tails are the coin's tails held long, which is why Calmar fails (0.39).
