---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-05_failed-breakout-multiday-drift.d1_failure-still-below-high
line: 7.d not profitable
backtest: 029-05_failed-breakout-multiday-drift.d1_failure-still-below-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a close back below the old 20-day high within 3 days of a breakout above it, the coin's decline continues across the following 8 days only while its close 2 days after the failure is still below that old high. The calmer the coin's past 30 days, the larger the fall from day 2 to day 10.
Consequence: A trader would short a failed breakout that stays below the old high mainly when the coin has been quiet, and would refuse the short when its recent volatility is high.
Why:
- F1: The book loses because the move it captures is smaller than its cost. Per case over 8 days the short earned a total of -0.14 % (489 cases; unusual move +0.91 %), against a cost of 0.19 % per trade. The coin's normal drift (-1.05 % in the short's direction) cancels the small unusual move. The result is a mean daily book return of -0.0091 % and a Sharpe of -0.14.
- F3: The cases split by the coin's 30-day volatility, and the gain falls as volatility rises. The total short move per case was +1.45 % (t 1.58, 103 cases) in the calmest quarter, then -0.41 % and -0.54 % in the middle quarters, and -1.93 % (t -1.31, 103 cases) in the most volatile quarter.
- F2: The book's 995 trades lost 2.94 % each before fees and 3.04 % after (29 % winners, held 6.4 days on average). That is far worse than the -0.14 % per case. The book does more than miss a small edge: the trades it actually holds lose heavily.
