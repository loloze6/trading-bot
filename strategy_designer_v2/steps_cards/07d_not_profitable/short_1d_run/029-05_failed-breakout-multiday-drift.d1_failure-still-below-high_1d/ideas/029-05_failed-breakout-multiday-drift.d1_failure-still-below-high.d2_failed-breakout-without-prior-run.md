---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-05_failed-breakout-multiday-drift.d1_failure-still-below-high
line: 7.d not profitable
backtest: 029-05_failed-breakout-multiday-drift.d1_failure-still-below-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a close back below the old 20-day high within 3 days of a breakout above it, the coin's decline continues across the following 8 days only while its close 2 days after the failure is still below that old high. The smaller the coin's 20-day return before the breakout, the larger the fall from day 2 to day 10.
Consequence: A trader would short a failed breakout that follows a flat month, and would refuse it when the breakout came on top of a strong 20-day rise, which tends to be bought again.
Why:
- F1: The book loses because the move it captures is smaller than its cost. Per case over 8 days the short earned a total of -0.14 % (489 cases; unusual move +0.91 %), against a cost of 0.19 % per trade. The coin's normal drift (-1.05 % in the short's direction) cancels the small unusual move. The result is a mean daily book return of -0.0091 % and a Sharpe of -0.14.
- F4: The cases also split by the coin's prior 20-day return. Shorts after a 20-day return under 2.3 % earned +1.64 % per case (t 1.41, 103 cases). Shorts after a 9.7 %-19.5 % rise lost 2.74 % (t -2.83, 102 cases). Shorts when the coin stood 8.6 %-23.7 % above its 100-day mean lost 3.85 % (t -2.46, 61 cases).
- F2: The book's 995 trades lost 2.94 % each before fees and 3.04 % after (29 % winners, held 6.4 days on average). That is far worse than the -0.14 % per case. The book does more than miss a small edge: the trades it actually holds lose heavily.
