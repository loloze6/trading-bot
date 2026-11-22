---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only
line: 7.g patterns
backtest: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The more a coin rises over the four hours before 00:00 UTC, measured in its usual four-hour move over the past 30 days, the more it falls over the next four hours.
Consequence: A trader refuses to buy a coin that has just risen strongly into the UTC midnight, and stays short of it for the following four hours.
Why:
- F1: The 4 hours after 00:00 UTC fall below the coin's average by -0.071 % (t -4.62, 17373 bars), and the fall grows with the size of the rise over the 4 hours before 00:00 UTC: from -0.009 % (t -0.22) in the lowest quintile of that prior move to -0.150 % (t -4.45) and -0.207 % (t -5.08, 3273 bars each) in the top two. It holds in five of six coins (XRP -0.143 %, t -3.66; ZEC -0.117 %, t -2.47; BTC -0.066 %, t -2.58), but it was strongest in 2018 (-0.302 %, t -5.44) and 2022 (-0.171 %, t -4.20) and turned slightly positive in 2023 to 2025 (up to +0.072 %, t 1.96).
