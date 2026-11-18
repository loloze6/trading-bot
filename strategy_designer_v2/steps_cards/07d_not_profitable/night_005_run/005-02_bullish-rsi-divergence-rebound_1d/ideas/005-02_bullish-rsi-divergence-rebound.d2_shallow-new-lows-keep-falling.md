---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close makes a new 30-day low, the smaller its 30-day decline into that low, the further it keeps falling over the next 10 days.
Consequence: A new low reached after only a mild fall is a reason to refuse a rebound long, and a reason to expect continuation.
Why:
- F5: Across all 87 new 30-day lows, the shallow-decline tercile (30-day return -5.1%) went on to fall 3.78% below the coin's mean 10-day return (t -1.89, n=29). The deep-decline tercile (30-day return -29.6%) was flat at +0.08% (t 0.03, n=29).
- F3: Inside the divergence cases, the depth of the prior 30-day fall grades the rebound. The deepest tercile of 30-day return (mean -34%) gained +4.56% over 10 days, +3.28% above the coin's mean (t 0.82, n=15). The shallowest tercile (mean -9.9%) lost -2.24%, -3.49% below the coin's mean (t -1.37, n=15). The Spearman correlation of the 14-day return with the 10-day return was -0.31.
