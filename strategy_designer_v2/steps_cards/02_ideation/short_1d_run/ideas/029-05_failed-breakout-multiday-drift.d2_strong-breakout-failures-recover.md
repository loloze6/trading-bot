---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-05_failed-breakout-multiday-drift
line: 7.d not profitable
backtest: 029-05_failed-breakout-multiday-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a close back below the old 20-day high within 3 days of a breakout above it, the coin rises over the following 10 days. The further the breakout's highest close had extended above the old high, the larger the rise.
Consequence: A short trader would refuse to short the failure of a strong breakout, because that failure tends to be bought and broken again.
Why:
- F5: The failures of the strongest breakouts are followed by the largest rise. In the top third of breakout extension above the old high, the unusual move over days 0 to 10 is -4.52 % (t -2.39). In the lowest third it is +0.38 % (t 0.39).
- F4: Which way the drift runs is decided by where price stands at day 2. When the coin is already back above the old high at day 2 (31.5 % of failures), it keeps rising over days 2 to 10, with an unusual move of -4.27 % (t -2.37, 148 cases); that is the second, successful break the brief names as its refutation. When it is still below the old high, days 2 to 10 give +0.76 % (t 1.20, 322 cases).
- F1: The book loses because the coin rises after the bet is placed, and costs are not the reason. Per case the total short-side move over 8 days is -1.42 %, which is -7.3 times the 0.19 % cost of a trade. The unusual move is -0.36 % (t -0.52, 539 cases), and my recomputation gives -0.68 % (t -0.94, 496 cases). Across 1193 trades the mean is -4.29 % before fees and -4.39 % after, with 29.5 % winners.
