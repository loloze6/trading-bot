---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only.b1_deep-fading-down-streak-rebound
line: 7.g patterns
backtest: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only.b1_deep-fading-down-streak-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The wider a coin's bar ranges over its past day relative to their 30-day average, the more the coin rises over the next three days.
Consequence: A trader leans long after a day of expanded ranges and stays out after a compressed, quiet day.
Why:
- F3: The bar range over the last day, against its 30-day mean, behaves like volume and is slightly stronger: rank correlation +0.073 with the next 3 days' excess return, positive in all six coins (0.045 to 0.093); the top fifth is followed by +0.78 % (t 2.19) and the bottom fifth by −0.67 % (t −2.70); it keeps t 2.13 in a joint regression in which volume drops to t 1.19.
