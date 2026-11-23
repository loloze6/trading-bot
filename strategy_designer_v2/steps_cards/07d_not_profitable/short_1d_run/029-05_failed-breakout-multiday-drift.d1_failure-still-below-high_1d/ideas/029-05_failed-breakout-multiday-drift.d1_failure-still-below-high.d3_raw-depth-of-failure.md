---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-05_failed-breakout-multiday-drift.d1_failure-still-below-high
line: 7.d not profitable
backtest: 029-05_failed-breakout-multiday-drift.d1_failure-still-below-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a close back below the old 20-day high within 3 days of a breakout above it, the coin's decline continues across the following 8 days only while its close 2 days after the failure is still below that old high. The further that day-2 close sits below the old high, in percent of price and not against its own recent history, the larger the fall from day 2 to day 10.
Consequence: A trader would size the short by the raw depth below the old high and would barely short a failure sitting just under it.
Why:
- F5: The shallowest failures lose. Cases whose close sat 0 % to 1.7 % below the old high lost 2.67 % per case (t -2.22, 123 cases), while deeper cases earned +0.36 % to +1.64 %. Yet the standardised forecast sat at its cap of 20 in at least three quarters of the cases, so the book gave shallow and deep failures the same size.
- F2: The book's 995 trades lost 2.94 % each before fees and 3.04 % after (29 % winners, held 6.4 days on average). That is far worse than the -0.14 % per case. The book does more than miss a small edge: the trades it actually holds lose heavily.
