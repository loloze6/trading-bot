---
brief: 016_grind-versus-jump-moves
source-idea: 016-02_down-grind-price-continuation
line: 7.g patterns
backtest: 016-02_down-grind-price-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Each coin rises over the two hours from 21:00 to 23:00 UTC, and the higher its hourly volatility over the past 7 days, the larger that rise.
Consequence: A trader can hold the coin long over that two-hour slot each day, sized up when the coin has been volatile over the past week.
Why:
- F1: Every coin rises in the two hours from 21:00 to 23:00 UTC. The coin-average return per timestamp is +0.055% in hour 21 (t 3.38, n 2920) and +0.045% in hour 22 (t 2.97, n 2918), and no other hour reaches |t| 2.1 once averaged across coins. On a non-overlapping daily sample of the 2-hour return taken at the 20:00 close, each coin is positive on its own: BTC +0.082% (t 4.39), ETH +0.114% (t 4.73), LTC +0.101% (t 3.83), XMR +0.096% (t 3.47), XRP +0.098% (t 3.14) and ZEC +0.107% (t 3.31), with about 2,700 days each. The effect is positive in 7 of 8 years; 2022 is the exception at −0.022% (t −0.68).
- F2: The 21:00–23:00 UTC rise grows with the coin's 7-day hourly volatility. By volatility quartile it is +0.029% (t 2.29), +0.079% (t 4.82), +0.079% (t 3.64) and +0.212% (t 6.53), with about 4,100 days per quartile. Scaled by that volatility, it is still largest in the top quartile: 0.124 against 0.078 in the bottom quartile.
