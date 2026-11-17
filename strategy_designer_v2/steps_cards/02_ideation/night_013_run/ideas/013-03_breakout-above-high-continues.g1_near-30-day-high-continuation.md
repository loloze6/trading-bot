---
brief: 013_anchoring-to-recent-high
source-idea: 013-03_breakout-above-high-continues
line: 7.g patterns
backtest: 013-03_breakout-above-high-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's daily close is to the highest high of its prior 30 days, the larger the coin's return over the next 10 days. The effect continues, growing with the distance, for closes that clear that high.
Consequence: A trader would lean long on coins pressing against or just through their 30-day high for about a 10-day hold, and refuse longs on coins well below it.
Why:
- F1: The pattern sits at a 30-day high, not a 52-week one. Bars in the top quintile of distance from the prior 30-day high (a mean of -1.0%, so almost at the high) beat the coin's average 10-day return by +3.34% (t 2.73, n 245 non-overlapping cases). The other four quintiles all came out between -0.56% and -1.02%.
- F2: Inside the near-high zone the effect is graded. On bars closing within 5% of the prior 30-day high, the slope of 10-day excess return on that distance is 1.41 (t 5.31, n 244), the strongest result across both rounds.
- F3: The top-quintile excess does not depend on the sampling grid. Across all 10 offsets of the 10-day grid it stays positive, between +1.77% and +3.34%, with top-quintile t from 1.38 to 2.83 and slope t from 0.59 to 2.92.
- F4: The effect is short-lived and needs a short lookback.
- F5: Closes above the prior 30-day high mostly continue. 65% were still above that level 10 days later, and they beat the coin's average 10-day return by +7.37% (t 2.37, n 69).
