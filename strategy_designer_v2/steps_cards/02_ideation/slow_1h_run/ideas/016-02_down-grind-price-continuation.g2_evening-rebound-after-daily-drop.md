---
brief: 016_grind-versus-jump-moves
source-idea: 016-02_down-grind-price-continuation
line: 7.g patterns
backtest: 016-02_down-grind-price-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over the past 24 hours relative to its own volatility, the more it rises over the two hours from 21:00 to 23:00 UTC that follow.
Consequence: A coin that has dropped hard during the day is a candidate for a short long position into the 21:00–23:00 UTC hours.
Why:
- F1: Every coin rises in the two hours from 21:00 to 23:00 UTC. The coin-average return per timestamp is +0.055% in hour 21 (t 3.38, n 2920) and +0.045% in hour 22 (t 2.97, n 2918), and no other hour reaches |t| 2.1 once averaged across coins. On a non-overlapping daily sample of the 2-hour return taken at the 20:00 close, each coin is positive on its own: BTC +0.082% (t 4.39), ETH +0.114% (t 4.73), LTC +0.101% (t 3.83), XMR +0.096% (t 3.47), XRP +0.098% (t 3.14) and ZEC +0.107% (t 3.31), with about 2,700 days each. The effect is positive in 7 of 8 years; 2022 is the exception at −0.022% (t −0.68).
- F3: The 21:00–23:00 UTC rise is largest after the coin's steepest falls over the past 24 hours, measured relative to its volatility. In the lowest quintile of that move it is +0.207% (t 6.92, n 3282), against +0.07% to +0.11% in the other four quintiles.
