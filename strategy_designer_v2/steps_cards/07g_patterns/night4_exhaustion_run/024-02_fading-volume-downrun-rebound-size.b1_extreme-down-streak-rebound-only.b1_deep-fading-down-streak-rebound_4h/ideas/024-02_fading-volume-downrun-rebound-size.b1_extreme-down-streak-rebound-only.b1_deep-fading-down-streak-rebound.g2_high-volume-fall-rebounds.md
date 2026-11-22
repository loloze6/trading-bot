---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only.b1_deep-fading-down-streak-rebound
line: 7.g patterns
backtest: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only.b1_deep-fading-down-streak-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: After a coin falls over its past day, the higher that day's volume relative to the coin's 30-day average, the larger the coin's rise over the next three days.
Consequence: A trader buys a one-day fall on heavy volume as a capitulation that rebounds, and refuses to buy a fall on thin volume.
Why:
- F2: The volume effect is strongest after a falling day: when the last day's return was negative, the top quarter of volume is followed by +1.16 % excess over 3 days (t 3.09, 645 cases) and the bottom quarter by −0.60 % (t −1.82); after a rising day the top quarter gives only +0.49 % (t 1.25); the rank correlation is 0.079 after falls and 0.051 after rises.
- F4: The last day's return, in usual moves, reverses over the next 3 days: rank correlation −0.053 (p 0.0001, 5292 cases); the bottom fifth (the sharpest one-day falls) is followed by +0.79 % excess (t 2.76, 1059 cases); in the joint regression it keeps t −3.37, while the 3-day past return carries the opposite sign (t +3.54).
